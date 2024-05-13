import boto3
from utils import utils
from config import bot, settings
from aiogram.types import InputFile
from common.classes import ServicePhotos
from typing import Union
from io import BytesIO


class S3DB:

    __BUCKET_NAME: str = "findit-bucket"

    @property
    def __client(self) -> Union[boto3.client]:
        return boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
        )

    async def save_preview(
            self,
            file_id: str,
            announcement_id: str
    ):
        buffer = BytesIO()
        photo_path = await bot.get_file(
            file_id
        )

        await bot.download_file(
            photo_path.file_path,
            buffer
        )
        self.__client.upload_fileobj(
            buffer,
            self.__BUCKET_NAME,
            f"announcements/{announcement_id}.png"
        )

    def get_preview(
            self,
            announcement_id: str
    ):
        buffer = BytesIO()

        try:
            self.__client.download_fileobj(
                self.__BUCKET_NAME,
                f"announcements/{announcement_id}.png",
                buffer
            )
        except:
            return utils.get_photo(
                ServicePhotos.UNKNOWN_ANNOUNCEMENT
            )

        buffer.seek(0)

        return InputFile(
            buffer
        )


blob = S3DB()

