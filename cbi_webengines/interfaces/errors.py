from pydantic import BaseModel

from cbi_ddd.interfaces.errors import Error


class EngineErrorData(BaseModel):
    code: str
    message: str
    args: dict


class EngineError(Error):
    status_code: int = 200
    code: str = 'UNKNOWN_ERROR'
    message: str = 'Unknown error'
    args: dict = {}

    def __init__(
        self,
        status_code: int,
        code: str,
        message: str,
        args: dict = {},
        *objects: object
    ) -> None:
        self.status_code = status_code
        self.code = code
        self.message = message
        self.args = args

        super().__init__(*objects)

    @property
    def data(self) -> EngineErrorData:
        return EngineErrorData(
            code=self.code,
            message=self.message,
            args=self.args,
        )


class NotFoundEngineError(EngineError):
    def __init__(self, args: dict = {}, *objects: object) -> None:
        super().__init__(
            404,
            'NOT_FOUND',
            'Unknown route',
            args,
            *objects
        )
