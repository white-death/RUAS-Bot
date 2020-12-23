from info import *
from discord_webhooks import DiscordWebhooks

#Put your discord webhook url here.

webhook_url = ''


def send_msg(class_name,status,current_time,start_time,end_time):

    WEBHOOK_URL = webhook_url 

    webhook = DiscordWebhooks(WEBHOOK_URL)
    # Attaches a footer
    webhook.set_footer(text='')

    if(status=="joined"):

      webhook.set_content(title='{} Class Joined Succesfully'.format(class_name),
                          description="Here's your report with :heart:")

      # Appends a field
      webhook.add_field(name='Class', value=class_name)
      webhook.add_field(name='Status', value=status)
      webhook.add_field(name='Expected Join time', value=start_time)
      webhook.add_field(name='Joined at', value=current_time)
      webhook.add_field(name='Leaving at', value=end_time)

    elif(status=="left"):
      webhook.set_content(title='Class left Succesfully',
                          description="Here's your report with :heart:")

      # Appends a field
      webhook.add_field(name='Class', value=class_name)
      webhook.add_field(name='Status', value=status)
      webhook.add_field(name='Expected Join time', value=start_time)
      webhook.add_field(name='Left at', value=end_time)


    elif(status=="noclass"):
      webhook.set_content(title='Seems like no {} today'.format(class_name),
                          description="No join button found! Assuming no class.")

      # Appends a field
      webhook.add_field(name='Class', value=class_name)
      webhook.add_field(name='Status', value=status)
      webhook.add_field(name='Last time of attempt', value=current_time)
      webhook.add_field(name='Expected Join time', value=start_time)
      webhook.add_field(name='Expected Leave time', value=end_time)

    elif(status=="saturday"):
      webhook.set_content(title='Holiday!',
                          description="Enjoy :heart:")

      # Appends a field
      webhook.add_field(name='Class', value=class_name)
      webhook.add_field(name='Status', value=status)
      webhook.add_field(name='Started at', value=start_time)
      webhook.add_field(name='Ending at', value=end_time)

    elif(status=="sunday"):
      webhook.set_content(title='Holiday!',
                          description="Enjoy :heart:")

      # Appends a field
      webhook.add_field(name='Class', value=class_name)
      webhook.add_field(name='Status', value=status)
      webhook.add_field(name='Started at', value=start_time)
      webhook.add_field(name='Ending at', value=end_time)



    webhook.send()

    print("Message sent to discord server")