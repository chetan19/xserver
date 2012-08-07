from django.db import models

import json

MAX_CHARFIELD_LEN = 1024

class Submission(models.Model):
    '''
    Representation of submission request, including metadata information
    '''
    # Submission 
    queue_name    = models.CharField(max_length=MAX_CHARFIELD_LEN)
    xqueue_header = models.CharField(max_length=MAX_CHARFIELD_LEN)
    xqueue_body   = models.TextField()

    # Uploaded files
    s3_keys = models.CharField(max_length=MAX_CHARFIELD_LEN) # S3 keys for internal Xqueue use
    s3_urls = models.CharField(max_length=MAX_CHARFIELD_LEN) # S3 urls for external access

    # Timing
    arrival_time = models.DateTimeField(auto_now=True) # Time of arrival from LMS
    pull_time   = models.DateTimeField(null=True, blank=True)  # Time of pull request, if pulled from external grader
    push_time   = models.DateTimeField(null=True, blank=True)  # Time of push, if xqueue pushed to external grader
    return_time = models.DateTimeField(null=True, blank=True)  # Time of return from external grader

    # External pull interface
    grader  = models.CharField(max_length=MAX_CHARFIELD_LEN) # ID of external grader
    pullkey = models.CharField(max_length=MAX_CHARFIELD_LEN) # Secret key for external pulling interface

    # Status
    num_failures = models.IntegerField(default=0) # Number of failures in exchange with external grader
    lms_ack = models.BooleanField(default=False)  # True/False on whether LMS acknowledged receipt

    def __unicode__(self):
        submission_info  = "Submission for queue '%s':\n" % self.queue_name
        submission_info += "    Arrival time: %s\n" % self.arrival_time
        submission_info += "    Pull time:    %s\n" % self.pull_time
        submission_info += "    Push time:    %s\n" % self.push_time
        submission_info += "    Return time:  %s\n" % self.return_time
        submission_info += "Xqueue header follows:\n"
        submission_info += json.dumps(json.loads(self.xqueue_header), indent=4)
        return submission_info
