
import fair_bpm

class FeedDog(fair_bpm.Activity):
    def execute(self, context=None):
        print("Starting feed dog")
        # Put feed dog code here

class WaterDog(fair_bpm.Activity):
    def execute(self, context=None):
        print("Starting water dog")
        # Put water dog code here

class MedicateDog(fair_bpm.Activity):
    def execute(self, context=None):
        print("Starting medicate dog")
        # Put medicate dog code here
        # Set Pills Left in context

class OrderMedication(fair_bpm.Activity):
    def execute(self, context=None):
        print("Starting order_medication dog")
        # Put order_medication dog code here
