# TruckX_Internship_Assignment

I am using twisted to implement the implementing REST API which takes request from the client and then work on given information. 
Every time new camera logs in new object is created and stored which handles recording alarm for this camera, uploading video for this camera and uploading location for this camera and when camera logs out ( Assumed that camera sends log off info before turning off so that we can remove it's object from online_cameras list )
After logging out the camera object is removed from the storage ( marked as offline ). 

Camera class implements interface for dealing with information sent by each camera and implements following methods

update_location
invoke_alarms
upload_video

these method connect with data base and update data base with given info about the camera. 

AdminUI class implements API so that Administrator UI can get the alarms of particular camera it takes id ( imei ) of camera for which the info is required. AdminUI class implements the following methods.
get_alarms
get_alarms_filter
get_recorded_videos
send_command
