AWS Project: VPC with Public & Private Subnets (Production Setup)

This project demonstrates how to set up a production-style VPC with both public and private subnets on AWS. The goal is to launch application servers in private subnets, expose them through a load balancer, and connect via a bastion host.

Architecture Overview

We’ll build this architecture step by step:

Create a VPC with public & private subnets.

Launch instances in Auto Scaling Groups (private subnets).

Configure a Bastion/Jump Host for secure access.

Set up an Application Load Balancer (ALB).

Access the deployed application via the ALB.

Step 1: Create VPC

Go to VPC and click Create VPC.

Select VPC and more option – AWS will suggest subnets, route tables, internet gateway, etc. Preview the settings.

<img width="1234" height="370" alt="Screenshot from 2025-09-17 16-00-26" src="https://github.com/user-attachments/assets/cfb3d94c-191a-4488-962b-4b06a7c6edad" />

Name the VPC and set the IP range (I used 10.0.0.16/16, ~65,536 IPs).

Keep default settings:

Availability Zones: 2

Public Subnets: 2

Private Subnets: 2

NAT Gateways: 1 per AZ

VPC Endpoints: None (for now)

Click Create VPC and watch AWS set everything up.

Step 2: Launch Instances in Auto Scaling Groups (Private Subnets)

Open EC2 → Auto Scaling Groups → Create Launch Template.

Configure the template:

Name & description

AMI: Ubuntu (example)

Instance type: t2.micro (Free Tier eligible)

Key pair (to SSH into server)

Security Group: allow Port 22 (SSH), Port 8000 (app)

[Important] Select the same VPC created earlier

Create the Launch Template.

Now create an Auto Scaling Group using that template:

Select the VPC

Choose Availability Zones → private subnets

No Load Balancer (for now)

Desired/Min/Max capacity → set according to expected load

Skip scaling policies (default)

Wait until the Auto Scaling Group launches instances.
Verify EC2 instances → they should be in private subnets.

<img width="677" height="466" alt="Screenshot from 2025-09-17 16-54-37" src="https://github.com/user-attachments/assets/ea7fe4c5-fed1-400b-b94d-729e2a80fa1b" />

⚠️ Note: These instances won’t have public IPs, so you cannot SSH directly. That’s where the Bastion Host comes in.

<img width="557" height="136" alt="Screenshot from 2025-09-17 17-35-07" src="https://github.com/user-attachments/assets/0230fc79-98eb-4391-abfa-1b36cf122c64" />
Step 3: Bastion/Jump Host

Go to EC2 → Launch Instance.

Configure:

Ubuntu image, t2.micro

Provide key pair

Security group: allow SSH (Port 22)

VPC: same VPC as application instances

Enable Auto-assign Public IP

Launch the instance.

SSH into the Bastion Host.

Now, to SSH into private EC2 instances:

Copy your private key into the Bastion Host using scp:

scp /path/to/local/key.pem user@<bastion-public-ip>:/home/ubuntu/


From the Bastion Host, SSH into private instances using their private IPs.

<img width="512" height="124" alt="Screenshot from 2025-09-17 17-43-04" src="https://github.com/user-attachments/assets/1fc8da36-7a2e-43c6-89ee-567208c3cefd" />

✅ Once inside, you can host a simple web application on Port 8000.

Step 4: Create Load Balancer

Go to EC2 → Load Balancers → Create Load Balancer.

Choose Application Load Balancer.

Configure:

Name: choose something meaningful

Scheme: Internet-facing

IP type: IPv4

VPC: your project’s VPC

Availability Zones: select both public subnets

Security Group: allow Port 8000

Configure Listeners & Target Groups:

Listener: HTTP, Port 8000

Create a Target Group:

Type: Instances

Protocol: HTTP, Port 8000

Select VPC & register private EC2 instances

Go back to the ALB config:

Add another Listener: HTTP, Port 80 (to expose the ALB publicly)

Forward traffic to the Target Group created above

⚠️ Don’t forget: allow Port 80 in the ALB security group else it will be not reachable

<img width="985" height="248" alt="Screenshot from 2025-09-17 18-29-12" src="https://github.com/user-attachments/assets/945c7217-814b-4392-8ceb-0cab2ff30d1e" />
Step 5: Access the Application

Copy the DNS name/URL from the Load Balancer.

<img width="631" height="164" alt="Screenshot from 2025-09-17 18-30-37" src="https://github.com/user-attachments/assets/faec3b66-7a0c-4297-9f74-164f299d4847" />

Open it in the browser → you should see your app running on Port 8000, exposed via Port 80 on the ALB.

<img width="612" height="113" alt="Screenshot from 2025-09-17 18-31-17" src="https://github.com/user-attachments/assets/af15a341-f778-478d-8c7b-e814f94c2600" />

🎉 Congratulations! You just deployed a production-style VPC project with private subnets, bastion host, and an application load balancer.

Bonus Tip

To test load balancing:

Change the app text (e.g., "MY FIRST AWS" → "MY SECOND AWS") on different servers.

Refresh or put load on the site → watch the load balancer distribute traffic.
