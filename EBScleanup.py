import boto3
#written in python 2.7
# Set the global variables
globalVars  = {}

globalVars['REGION_NAME']           = "eu-west-3"


ec2       = boto3.resource('ec2', region_name = globalVars['REGION_NAME'] )

def lambda_handler(event, context):

    deletedVolumes=[]

    # Get all the volumes in the region
    for vol in ec2.volumes.all():
        if  vol.state=='available':

            # Check for Tags
           # if vol.tags is None:
                vid=vol.id
                v=ec2.Volume(vol.id)
                v.delete()

                deletedVolumes.append({'VolumeId': vol.id,'Status':'Delete Initiated'})
                print "Deleted Volume: {0} for not having Tags".format( vid )

              

    # If no Volumes are deleted, to return consistent json output
    if not deletedVolumes:
        deletedVolumes.append({'VolumeId':None,'Status':None})

    # Return the list of status of the snapshots triggered by lambda as list
    return deletedVolumes

