# 🧹 AWS Resource Cleanup Scripts (Python 3.11)

This repository provides modular Python 3.11 scripts to clean up **unused, orphaned, or idle AWS resources** — helping reduce cost and improve cloud hygiene.

---

## 📁 Included Scripts (Filename Mapping)

| Filename | What it Cleans |
|----------|----------------|
| `cleanstoppedec2.py` | Stopped EC2 instances |
| `cleanupIdelCWgroup.py` | Idle CloudWatch Log Groups |
| `cleanupNATgateway.py` | Unused NAT Gateways & Internet Gateways |
| `old+unusedSnapshot.py` | Old/unlinked EBS snapshots |
| `oldlaunch+configtemplate.py` | Unused Launch Templates & Configs |
| `orphanedTG.py` | Orphaned ELB Target Groups |
| `orphaseIamrole+policies.py` | Orphaned IAM Roles & Inline Policies |
| `unattachedebs.py` | Unattached EBS volumes |
| `unused+emptys3.py` | Empty/unused S3 buckets |
| `unusedAMI+snapshot.py` | Unused AMIs & their snapshots |
| `unusedEIP.py` | Unassociated Elastic IPs |
| `unusedLB.py` | Unused Load Balancers (ALB, NLB, Classic ELB) |
| `unusedLambdafunc.py` | Unused Lambda functions (based on CloudWatch invocations) |
| `unusedSG.py` | Unused Security Groups |
| `unusedrds.py` | Stopped RDS Instances |
| `unusedsecretSSM.py` | Old/unused Secrets in Secrets Manager |
| `securitygrpscan.py` | Scan all AWS regions for security groups with port 22 (SSH) open to the world |

---

## ⚠️ Precautions Before Use

- ✅ **Always tag resources to keep** with:  
  `Key = Keep`, `Value = True`
- ✅ Use **sandbox/test environment** before applying in production
- ✅ Review logs after dry-run or first execution
- ❌ Never delete resources you don't own or fully understand

---

## 🔧 Requirements

Install dependencies:

```bash
pip install boto3


python3 <script_name>.py

python3 unusedEIP.py


🛡 IAM Permissions Required
Ensure your user/role has permissions to:

ec2:*Describe*, ec2:Delete*, ec2:Release*

iam:*

rds:*

s3:*

lambda:*

logs:*

secretsmanager:*

elasticloadbalancing:*

autoscaling:*

cloudwatch:GetMetricStatistics


Ankit Gupta
GitHub: Rajeshgupta123456789

📬 Contribute / Report Issues
PRs and issues are welcome!
Use this responsibly and automate only with tagging + approvals in production.


Let me know if you want a matching `requirements.txt` or auto-link each filename in GitHub Markdown


