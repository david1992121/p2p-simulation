import unittest
from fastapi import Response
from app.main import get_application, route_application
from fastapi.testclient import TestClient

app = get_application()
route_application(app)

client = TestClient(app)


class TestAPI(unittest.TestCase):
    '''
    A class for testing API
    '''

    def setUp(self):
        self.first_capacity = 1
        self.second_capacity = 2

    def test_join_leave(self):
        self.join(self.first_capacity)
        response = self.get_status()
        assert response.json() == [
            {
                "nodes": {
                    "N1": self.first_capacity
                },
                "edges": []
            }
        ]

        self.join(self.second_capacity)
        response = self.get_status()
        assert response.json() == [
            {
                "nodes": {
                    "N1": self.first_capacity,
                    "N2": self.second_capacity
                },
                "edges": [
                    [
                        "N1",
                        "N2"
                    ]
                ]
            }
        ]

        self.leave(1)
        response = self.get_status()
        assert response.json() == [
            {
                "nodes": {
                    "N2": self.second_capacity
                },
                "edges": []
            }
        ]

    def join(self, capacity) -> Response:
        response = client.post("/network/join", json={"capacity": capacity})
        assert response.status_code == 200
        return response

    def leave(self, node_id):
        response = client.post("/network/leave", json={"id": node_id})
        assert response.status_code == 200
        return response

    def get_status(self):
        response = client.get("/network/status")
        assert response.status_code == 200
        return response
