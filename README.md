This script is a modified version of the example queries found here: https://docs.panther.com/panther-developer-workflows/api/operations/data-lake-queries#end-to-end-examples. It allows you to analyze your Panther detections to see how many of your enabled detections have generated rule matches over the past 30 days. 

### Example usage
```
python list_detections.py ~/desktop/panther-labs/panther-analysis
```
```
[{'count(*)': 2, 'p_rule_id': 'Panther.User.Modified'}, {'count(*)': 2, 'p_rule_id': 'Okta.APIKeyCreated'}, {'count(*)': 2, 'p_rule_id': 'Okta.APIKeyRevoked'}, {'count(*)': 3, 'p_rule_id': 'Panther.SAML.Modified'}, {'count(*)': 4, 'p_rule_id': 'AWS.EC2.SecurityGroupModified'}, {'count(*)': 5, 'p_rule_id': 'Panther.Detection.Deleted'}, {'count(*)': 20, 'p_rule_id': 'AWS.IAM.PolicyModified'}, {'count(*)': 22, 'p_rule_id': 'AWS.CloudTrail.IAMAnythingChanged'}, {'count(*)': 47, 'p_rule_id': 'Standard.BruteForceByIP'}, {'count(*)': 9224, 'p_rule_id': 'AWS.CloudTrail.UnauthorizedAPICall'}]
10 detections fired over the past 30 days!
```


### Option 1: Run the script over your panther-analysis repository

If you have a local copy of your panther-analysis repository, you can use this script to analyze the detections directly from the repository.

1. Download the script and save it on your local machine.
2. Open a terminal and navigate to the directory where you saved the script.
3. Run the script by typing the following command and replacing <path_to_panther_analysis> with the path to your panther-analysis repository:
```
python list_detections.py <path_to_panther_analysis>
```

The script will analyze the detections in your repository and query Panther to see how many of them have fired over the past 30 days.

### Option 2: Download your current detection set through Bulk Uploader

If you don't manage your Panther detections via a developer workflow, you can download your detection set through the Bulk Uploader in Panther and then use this script to analyze the detections. Here's how:

1. Log in to your Panther account.
2. Navigate to the Bulk Uploader page.
3. Click on `Download all entities`.
5. Save the downloaded file in a directory on your local machine.
6. Download the script and save it in the same directory.
Open a terminal and navigate to the directory where you saved the script and the detection set.
Run the script by typing the following command and replacing <path_to_detection_set> with the path to the downloaded entities:
```
python list_detections.py <path_to_detection_set>
```
The script will analyze the detections in the downloaded detection set and query Panther to see how many of them have fired over the past 30 days.

Please note that the script requires Python and the gql and aiohttp libraries to be installed on your machine. If you don't have these installed, you can install them by running the following command:

```
pip install gql aiohttp
```
Also, you need to ensure that you replace the placeholders in the script (**PANTHER_ENDPOINT** and **PANTHER_API_KEY**) with your actual Panther API URL and API key.
