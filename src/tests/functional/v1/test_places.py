import pytest
from starlette import status

from models import Place
from repositories.places_repository import PlacesRepository


@pytest.mark.usefixtures("session")
class TestPlacesCreateMethod:
    """
    Тестирование метода создания любимого места.
    """

    @staticmethod
    async def get_endpoint() -> str:
        """
        Получение адреса метода API.

        :return:
        """

        return "/api/v1/places"

    @pytest.mark.asyncio
    @pytest.mark.usefixtures("event_producer_publish")
    async def test_method_success(self, client, session, httpx_mock):
        """
        Тестирование успешного сценария.

        :param client: Фикстура клиента для запросов.
        :param session: Фикстура сессии для работы с БД.
        :param httpx_mock: Фикстура запроса на внешние API.
        :return:
        """

        mock_response = {
            "city": "City",
            "countryCode": "AA",
            "locality": "Location",
        }
        # замена настоящего ответа от API на "заглушку" для тестирования
        # настоящий запрос на API не производится
        httpx_mock.add_response(json=mock_response)

        # передаваемые данные
        request_body = {
            "latitude": 12.3456,
            "longitude": 23.4567,
            "description": "Описание тестового места",
        }
        # осуществление запроса
        response = await client.post(
            await self.get_endpoint(),
            json=request_body,
        )

        # проверка корректности ответа от сервера
        assert response.status_code == status.HTTP_201_CREATED

        response_json = response.json()
        assert "data" in response_json
        assert isinstance(response_json["data"]["id"], int)
        assert isinstance(response_json["data"]["created_at"], str)
        assert isinstance(response_json["data"]["updated_at"], str)
        assert response_json["data"]["latitude"] == request_body["latitude"]
        assert response_json["data"]["longitude"] == request_body["longitude"]
        assert response_json["data"]["description"] == request_body["description"]
        assert response_json["data"]["country"] == mock_response["countryCode"]
        assert response_json["data"]["city"] == mock_response["city"]
        assert response_json["data"]["locality"] == mock_response["locality"]

        # проверка существования записи в базе данных
        created_data = await PlacesRepository(session).find_all_by(
            latitude=request_body["latitude"],
            longitude=request_body["longitude"],
            description=request_body["description"],
            limit=100,
        )
        assert len(created_data) == 1
        assert isinstance(created_data[0], Place)
        assert created_data[0].latitude == request_body["latitude"]
        assert created_data[0].longitude == request_body["longitude"]
        assert created_data[0].description == request_body["description"]
        assert created_data[0].country == mock_response["countryCode"]
        assert created_data[0].city == mock_response["city"]
        assert created_data[0].locality == mock_response["locality"]

    @pytest.mark.asyncio
    @pytest.mark.usefixtures("event_producer_publish")
    async def test_auto(self, client, session, httpx_mock):
        """
        Тестирование сценария автоматического определения места.

        :param client: Фикстура клиента для запросов.
        :param session: Фикстура сессии для работы с БД.
        :param httpx_mock: Фикстура запроса на внешние API.
        :return:
        """

        mock_response = {
            "city": "City",
            "countryCode": "AA",
            "locality": "Location",
        }
        # замена настоящего ответа от API на "заглушку" для тестирования
        # настоящий запрос на API не производится
        httpx_mock.add_response(json=mock_response)

        # передаваемые данные
        request_body = {
            "description": "Описание любимого места",
        }

        # осуществление запроса
        response = await client.post(
            await self.get_endpoint() + "/auto",
            json=request_body,
        )

        # проверка корректности ответа от сервера
        assert response.status_code == status.HTTP_201_CREATED

        response_json = response.json()
        assert "data" in response_json
        local_coords = [
            response_json["data"]["latitude"],
            response_json["data"]["longitude"],
        ]
        assert isinstance(response_json["data"]["id"], int)
        assert isinstance(response_json["data"]["created_at"], str)
        assert isinstance(response_json["data"]["updated_at"], str)
        assert isinstance(response_json["data"]["latitude"], float)
        assert isinstance(response_json["data"]["longitude"], float)
        assert response_json["data"]["description"] == request_body["description"]
        assert response_json["data"]["country"] == mock_response["countryCode"]
        assert response_json["data"]["city"] == mock_response["city"]
        assert response_json["data"]["locality"] == mock_response["locality"]

        # проверка существования записи в базе данных
        created_data = await PlacesRepository(session).find_all_by(
            description=request_body["description"],
            limit=100,
        )
        assert len(created_data) == 1
        assert isinstance(created_data[0], Place)
        assert created_data[0].latitude == local_coords[0]
        assert created_data[0].longitude == local_coords[1]
        assert created_data[0].description == request_body["description"]
        assert created_data[0].country == mock_response["countryCode"]
        assert created_data[0].city == mock_response["city"]
        assert created_data[0].locality == mock_response["locality"]

    @pytest.mark.asyncio
    @pytest.mark.usefixtures("event_producer_publish")
    async def test_get_places(self, client, session):
        """
        Тестирование получения списка любимых мест.
        :param client: Фикстура клиента для запросов.
        :param session: Фикстура сессии для работы с БД.
        :return:
        """

        request_body = {
            "latitude": 12.3456,
            "longitude": 23.4567,
            "description": "Описание любимого места",
            "city": "City",
            "locality": "Location",
            "country": "AA",
        }

        await PlacesRepository(session).create_model(request_body)
        response = await client.get(
            await self.get_endpoint(),
        )

        assert response.status_code == status.HTTP_200_OK

        response_json = response.json()
        assert "items" in response_json
        assert isinstance(response_json["items"], list)
        assert len(response_json["items"]) > 0

        place = response_json["items"][len(response_json["items"]) - 1]
        assert isinstance(place["id"], int)
        assert isinstance(place["created_at"], str)
        assert isinstance(place["updated_at"], str)
        assert place["latitude"] == request_body["latitude"]
        assert place["longitude"] == request_body["longitude"]
        assert place["description"] == request_body["description"]
        assert place["country"] == request_body["country"]
        assert place["city"] == request_body["city"]
        assert place["locality"] == request_body["locality"]

        assert response_json["total"] > 0
        assert response_json["page"] == 1
        assert response_json["size"] == 50

    @pytest.mark.asyncio
    @pytest.mark.usefixtures("event_producer_publish")
    async def test_get_place(self, client, session):
        """
        Тестирование получения одного любимого места.
        :param client: Фикстура клиента для запросов.
        :param session: Фикстура сессии для работы с БД.
        :return:
        """
        mock_response = {
            "city": "City",
            "countryCode": "AA",
            "locality": "Location",
        }

        request_body = {
            "latitude": 12.3456,
            "longitude": 23.4567,
            "description": "Описание любимого места",
            "city": "City",
            "locality": "Location",
            "country": "AA",
        }

        place_id = await PlacesRepository(session).create_model(request_body)
        response = await client.get((await self.get_endpoint()) + f"/{place_id}")

        assert response.status_code == status.HTTP_200_OK

        response_json = response.json()
        assert "data" in response_json
        assert isinstance(response_json["data"]["id"], int)
        assert isinstance(response_json["data"]["created_at"], str)
        assert isinstance(response_json["data"]["updated_at"], str)
        assert response_json["data"]["latitude"] == request_body["latitude"]
        assert response_json["data"]["longitude"] == request_body["longitude"]
        assert response_json["data"]["description"] == request_body["description"]
        assert response_json["data"]["country"] == mock_response["countryCode"]
        assert response_json["data"]["city"] == mock_response["city"]
        assert response_json["data"]["locality"] == mock_response["locality"]

    @pytest.mark.asyncio
    @pytest.mark.usefixtures("event_producer_publish")
    async def test_delete_place(self, client, session):
        """
        Тестирование удаления любимого места.
        :param client: Фикстура клиента для запросов.
        :param session: Фикстура сессии для работы с БД.
        :return:
        """
        # передаваемые данные
        request_body = {
            "latitude": 12.3456,
            "longitude": 23.4567,
            "description": "Описание любимого места",
            "city": "City",
            "locality": "Location",
            "country": "AA",
        }
        place_id = await PlacesRepository(session).create_model(request_body)

        response = await client.delete((await self.get_endpoint()) + f"/{place_id}")

        assert response.status_code == status.HTTP_204_NO_CONTENT

        response = await client.get((await self.get_endpoint()) + f"/{place_id}")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.asyncio
    @pytest.mark.usefixtures("event_producer_publish")
    async def test_patch_place(self, client, session, httpx_mock):
        """
        Тестирование успешного сценария.
        :param client: Фикстура клиента для запросов.
        :param session: Фикстура сессии для работы с БД.
        :param httpx_mock: Фикстура запроса на внешние API.
        :return:
        """

        mock_response = {
            "city": "City",
            "countryCode": "AA",
            "locality": "Location",
        }
        httpx_mock.add_response(json=mock_response)

        request_body = {
            "latitude": 12.3456,
            "longitude": 23.4567,
            "description": "Описание любимого места",
            "city": "City",
            "locality": "Location",
            "country": "AA",
        }
        place_id = await PlacesRepository(session).create_model(request_body)

        patch_request_body = {
            "latitude": 12.3456,
            "longitude": 23.4567,
            "description": "Новое описание любимого места",
        }

        response = await client.patch(
            (await self.get_endpoint()) + f"/{place_id}", json=patch_request_body
        )

        assert response.status_code == status.HTTP_200_OK

        response_json = response.json()
        assert "data" in response_json
        assert isinstance(response_json["data"]["id"], int)
        assert isinstance(response_json["data"]["created_at"], str)
        assert isinstance(response_json["data"]["updated_at"], str)
        assert response_json["data"]["latitude"] == patch_request_body["latitude"]
        assert response_json["data"]["longitude"] == patch_request_body["longitude"]
        assert response_json["data"]["description"] == patch_request_body["description"]
        assert response_json["data"]["country"] == mock_response["countryCode"]
        assert response_json["data"]["city"] == mock_response["city"]
        assert response_json["data"]["locality"] == mock_response["locality"]
