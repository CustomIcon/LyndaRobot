__all__ = ["LydiaSession", "Session"]


class LydiaSession:
    def __init__(self, data, client):
        """
        AI Session Object
        """

        self._client = client
        self.id = data["session_id"]
        self.language = data["language"]
        self.available = data["available"]
        self.expires = data["expires"]

    def think_thought(self, text):
        """
        Processes user input and returns an AI text Response

        :type text: str
        :param text: The user input
        :raises: CoffeeHouseError
        :returns: The JSON response from the server
        :rtype: str
        """

        return self._client.think_thought(self.id, text)

    def __str__(self):
        """
        Returns an identifier uniquely specifying this session

        :returns: The session id
        :rtype: str
        """

        return self.id


Session = LydiaSession  # For compatibility
