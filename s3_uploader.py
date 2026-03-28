import boto3
import json
from datetime import datetime

def upload_summary(summary_data, bucket_name="demo-env-builder-dunsworth"):
    s3 = boto3.client("s3")
    
    # Create a report with timestamp
    report = {
        "generated_at": datetime.now().isoformat(),
        "environment": summary_data
    }
    
    # Convert to JSON string
    report_json = json.dumps(report, indent=2)
    
    # Create a unique filename using timestamp
    filename = f"demo-summary-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
    
    # Upload to S3
    s3.put_object(
        Bucket=bucket_name,
        Key=filename,
        Body=report_json
    )
    
    print(f"Report uploaded to S3: {filename}")
    return filename