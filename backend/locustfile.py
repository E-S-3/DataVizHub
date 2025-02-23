from locust import HttpUser, task, between

class APIUser(HttpUser):
    wait_time = between(1, 3)

    @task(2)
    def test_top_roi(self):
        self.client.get("/api/top-roi")

    @task(1)
    def test_top_budget(self):
        self.client.get("/api/top-budget")

    @task(1)
    def test_revenue_expenses(self):
        self.client.get("/api/revenue-expenses")

    @task(1)
    def test_fund_table(self):
        self.client.get("/api/fund-table")

    @task(1)
    def test_net_profit(self):
        self.client.get("/api/net-profit")
