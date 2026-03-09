from abc import ABC, abstractmethod

class CreditBureauAdapter(ABC):

    @abstractmethod
    def fetch_credit_report(self, bvn: str):
        pass