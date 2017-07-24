import my_appapi as appapi
             
class ac_control(appapi.my_appapi):

  def initialize(self):
    # self.LOGLEVEL="DEBUG"
    self.log("ac_control App")
    self.listen_state(self.presence_handler,"input_boolean.noone_home")
    self.listen_state(self.check_presence,"climate.downstairs")

  def presence_handler(self,entity,attribute, old,new, kwargs):
    if not old==new:
      if new=="off":
        self.log("turning off away mode someone is home.")
        self.call_service("climate/set_away_mode",entity_id="climate.downstairs",away_mode="false")

  def check_presence(self,entity,attribute,old,new,kwargs):
    current_state=self.get_state(entity,attribute="all")
    self.log("nest current state={}".format(current_state))
    self.log("current_state={}".format(current_state))
    if current_state["attributes"]["away_mode"]=="on":
      home_state=self.get_state("input_boolean.noone_home")
      if home_state=="off":
        self.log("Nest switched to away, but someone iss till home turning away mode off")
        self.call_service("climate/set_away_mode",entity_id="climate.downstairs",away_mode="false")
