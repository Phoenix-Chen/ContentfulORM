import time
import contentful_management
from io import BytesIO

class ContentfulManagementConnector:
    def __init__(self, token, space_id, environment):
        """Contentful connector through contentful_managementself.

            Args:
                token (str) : Contentful management API access token.
                space_id (str) : Contentful space ID.
                environment (str) : Contentful environment.

            Attributes:
                space (object) : A contentful_management.space.Space object.
                environment (object) : A contentful_management.environment.Environment object.

        """
        _client = contentful_management.Client(token)
        self.space = _client.spaces().find(space_id)
        self.environment = self.space.environments().find(environment)

    def create(self, obj):
        return obj.create(self.environment)

    def delete(self, obj):
        return obj.delete(self.environment)

    def publish(self, obj):
        return obj.publish(self.environment)

    def unpublish(self, obj):
        return obj.unpublish(self.environment)

    def query(self, model):
        return model.query(self.environment)

    def add(self, obj):
        pass

    # def upload_image(self, image, publish=True):
    #     """Upload an image to Contentful.
    #
    #         Args:
    #             image (bytes) : The image to be uploaded
    #             publish (boolean, optional) : Whether publish the image after upload. Defaults to True.
    #
    #         Returns:
    #             dict : Return asset_id and url if publish is set to True. Return asset_id if publish is set to False.
    #
    #     """
    #     asset_id = generate_filename(image)
    #     file = BytesIO(image)
    #     image_upload = self.space.uploads().create(file)
    #     asset = self.environment.assets().create(
    #         asset_id,
    #         {
    #             'fields': {
    #                 'title': {
    #                             'en-US': asset_id
    #                          },
    #                 'file': {
    #                     'en-US': {
    #                         'fileName': asset_id + '.png',
    #                         'contentType': 'image/png',
    #                         'uploadFrom': image_upload.to_link().to_json()
    #                     }
    #                 }
    #             }
    #         }
    #     )
    #     asset.process()
    #     if publish:
    #         if self.publish(asset):
    #             asset.reload()
    #             return {'asset_id': asset_id, 'url': asset.url()}
    #     return {'asset_id': asset_id}


    # def publish(self, obj):
    #     """Publish and entry/asset on Contentful
    #
    #         Args:
    #             obj (object) : A contentful_management.entry.Entry/contentful_management.asset.Asset object to be published
    #
    #         Returns:
    #             boolean : True if publish succeed, False otherwise.
    #
    #     """
    #
    #     for tries in range(RETRIES_LIMIT):
    #         try:
    #             obj.reload()
    #             obj.publish()
    #             if obj.is_published:
    #                 return True
    #         except Exception as e:
    #             print(e)
    #         time.sleep(WAIT_TIME)
    #         print('Retry publish...')
    #     return False
