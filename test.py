import pytest
import yaml
import os
import logging
import time
from prompt import load_prompt_from_yaml
from call_provider import CallProvider
# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Get YAML files from directory
config_dir = 'config_files'
yaml_files = [
    os.path.join(config_dir, f) 
    for f in os.listdir(config_dir) 
    if f.endswith(('.yaml', '.yml'))
]

@pytest.mark.parametrize("test_yaml", yaml_files)
def test_have_description(test_yaml):
    """Test that all YAML config files contain a description field"""
    try:
        # Log test start
        logger.info(f"Starting test for file: {test_yaml}")
        
        # Load YAML content
        with open(test_yaml, "r") as f:
            logger.debug(f"Opening file: {test_yaml}")
            data = yaml.safe_load(f)
            logger.debug(f"Loaded YAML content: {data}")
        
        # Validate description exists
        logger.info("Checking for description field")
        assert "description" in data, f"Missing description in {test_yaml}"
        
        # Log success details
        logger.info(f"Description found: {data['description']}")
        logger.debug(f"Full description content: {data['description']}")

    except yaml.YAMLError as ye:
        logger.error(f"YAML parsing error in {test_yaml}: {str(ye)}")
        pytest.fail(f"Invalid YAML syntax in {test_yaml}")
    except Exception as e:
        logger.error(f"Unexpected error processing {test_yaml}: {str(e)}", exc_info=True)
        pytest.fail(f"Test failed for {test_yaml} due to unexpected error")

@pytest.mark.parametrize("test_yaml", yaml_files, ids=lambda tc: yaml.safe_load(open(tc, "r"))["description"])
def test_eval_prompt(test_yaml):

    prompt_config = load_prompt_from_yaml(test_yaml)
    prompt = prompt_config.prompt
    providers = prompt_config.providers
    tests = prompt_config.tests
    for provider in providers:
        logger.info('Testing Prompt: {prompt} with provider: {provider}')
        for test in tests:
            answer = getattr(CallProvider(), provider.split(":")[0])(provider.split(":")[1], prompt.format(**test.vars))
            for a in test.asserts:
                if a['type']=="contain":
                    assert a['value'] in answer
            time.sleep(1)
                    
@pytest.mark.parametrize("test_yaml", yaml_files, ids=lambda tc: yaml.safe_load(open(tc, "r"))["description"])
def test_eval_prompt(test_yaml):
    """Test all prompts against providers with test cases from YAML"""
    try:
        # Load and log test configuration
        logger.info(f"Starting evaluation for config: {test_yaml}")
        prompt_config = load_prompt_from_yaml(test_yaml)
        logger.debug(f"Loaded prompt config: {prompt_config}")
        
        # Initialize test components
        prompt = prompt_config.prompt
        providers = prompt_config.providers
        tests = prompt_config.tests
        
        # Track overall test statistics
        total_tests = 0
        start_time = time.time()
        
        # Iterate through all test combinations
        for provider in providers:
            provider_type = provider.split(":")[0]
            provider_name = provider.split(":")[1]
            logger.info(f"Testing Prompt: '{prompt}' with Provider: {provider}")
            
            for test in tests:
                total_tests += 1
                # Format the prompt with test variables
                formatted_prompt = prompt.format(**test.vars)
                logger.debug(f"Test Variables: {test.vars}")
                logger.debug(f"Formatted Prompt: {formatted_prompt}")
                
                retry = 3
                loop = 0
                last_exception = None

                while loop < retry:
                    try:
                        # Attempt provider call
                        logger.info(f"Attempt {loop+1}/{retry} with {provider}")
                        call_start = time.time()
                        answer = getattr(CallProvider(), provider_type)(provider_name, formatted_prompt)
                        call_duration = time.time() - call_start
                        
                        # Log successful call
                        logger.debug(f"Provider call succeeded in {call_duration:.2f}s")
                        logger.debug(f"Response: {answer}")

                        # Validate assertions
                        all_assertions_passed = True
                        for assertion in test.asserts:
                            assert_type = assertion['type']
                            expected = assertion['value']
                            logger.debug(f"Checking {assert_type}: expecting '{expected}'")
                            
                            try:
                                if assert_type == "contain":
                                    assert expected in answer, f"'{expected}' not found in response"
                                    logger.debug("✅ Contain assertion passed")
                                # Add more assertion types here
                                
                            except AssertionError as ae:
                                logger.warning(f"Assertion failed: {str(ae)}")
                                all_assertions_passed = False
                                last_exception = ae

                        if all_assertions_passed:
                            logger.info("All assertions passed!")
                            break  # Exit retry loop on success

                    except Exception as e:
                        logger.error(f"🚨 Provider call failed: {str(e)}")
                        last_exception = e
                    finally:
                        loop += 1
                        if loop < retry and last_exception is None:
                            time.sleep(1)  # Rate limiting between attempts
                        elif loop < retry:
                            logger.info(f"⏳ Retrying in 1 second...")
                            time.sleep(1)

                # Final failure check after all retries
                if loop >= retry:
                    if last_exception:
                        error_msg = f"Failed after {retry} attempts. Last error: {str(last_exception)}"
                    else:
                        error_msg = f"Failed after {retry} attempts. Assertions did not pass"
                    pytest.fail(f"{error_msg} | Provider: {provider_name} | Prompt: {formatted_prompt}")
                    
                    
        # Final test summary
        duration = time.time() - start_time
        logger.info(f"Test completed: {total_tests} assertions for prompt: {prompt}")
        logger.info(f"Total test duration: {duration:.2f} seconds")
        
    except Exception as e:
        logger.error(f"Critical error in test setup: {str(e)}", exc_info=True)
        pytest.fail(f"Test setup failed: {str(e)}")