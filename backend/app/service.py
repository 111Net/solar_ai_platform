class CreditBureauService:

    def __init__(self, adapter):
        self.adapter = adapter

    def get_score(self, bvn):
        try:
            report = self.adapter.fetch_credit_report(bvn)
            return report.get("credit_score", 600)
        except Exception as e:
            # Log error properly
            return 600

is_flagged = Column(Boolean, default=False)
default_probability = Column(Float)