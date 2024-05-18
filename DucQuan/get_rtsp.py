"""This module is used to get the the information related to each camera on the same network."""
from typing import List

from onvif import ONVIFCamera # https://github.com/FalkTannhaeuser/python-onvif-zeep/blob/zeep/setup.py
# pip install --upgrade onvif_zeep

class CameraError(Exception):
    """**CameraError** is raised for errors on **Camera**."""

class Camera:
    """This class is used to get the information from all cameras discovered on this specific
    network."""

    def __init__(self, ip, user, password):
        """Constructor.

        Args:
            ip (str): Ip of the camera.
            user (str): Onvif login.
            password (str): Onvif password.
        Raises:
            CameraError: If could not connect to camera, credentials are not valid or ONVIF is not
            supported on camera.
        """
        try:
            self._mycam = ONVIFCamera(ip, 80, user, password, no_cache = True)
        except:
            raise CameraError("Could not connect to camera. Verify credentials and ONVIF support.")
        self._camera_media = self._mycam.create_media_service()
        self._camera_media_profile = self._camera_media.GetProfiles()
        # print(self._camera_media_profile)
        
    def GetDNS(self) -> str:
        """Find manufacturer of camera.

        Returns:
            str: Manufacturer.
        """
        resp = self._mycam.devicemgmt.GetDNS()
        # print(resp)
        return resp

    def detail_video(self) -> str:

        resp = self._camera_media.GetProfiles()[0]
        return resp.Name, resp.VideoEncoderConfiguration.Encoding, resp.VideoEncoderConfiguration.Resolution.Width, resp.VideoEncoderConfiguration.Resolution.Height ,\
                resp.VideoEncoderConfiguration.Quality, resp.VideoEncoderConfiguration.RateControl.FrameRateLimit, resp.VideoEncoderConfiguration.RateControl.BitrateLimit, \
                resp.VideoEncoderConfiguration.H264.GovLength, resp.VideoEncoderConfiguration.H264.H264Profile
    
    def GetUser(self) -> str:
        """
        Returns:
            'Username': 'admin',
            'Password': None,
            'UserLevel': 'Administrator',
            'Extension': None,
            '_attr_1': None
        """
        resp = self._mycam.devicemgmt.GetUsers()
        return resp[0].Username, resp[0].Password, resp[0].UserLevel

    def manufacturer(self) -> str:
        """Find manufacturer of camera.

        Returns:
            str: Manufacturer.
        """
        resp = self._mycam.devicemgmt.GetDeviceInformation()
        # print(resp)
        return resp.Manufacturer

    def model(self) -> str:
        """Find model of camera.

        Returns:
            str: Model.
        """
        resp = self._mycam.devicemgmt.GetDeviceInformation()
        # print(resp)
        return resp.Model

    def firmware_version(self) -> str:
        """Find firmware version of camera.

        Returns:
            str: Firmware version.
        """
        resp = self._mycam.devicemgmt.GetDeviceInformation()
        return resp.FirmwareVersion

    def mac_address(self) -> str:
        """Find serial number of camera.

        Returns:
            str: Serial number.
        """
        resp = self._mycam.devicemgmt.GetDeviceInformation()
        return resp.SerialNumber

    def hardware_id(self) -> str:
        """Find hardware id of camera.

        Returns:
            str: Hardware Id.
        """
        resp = self._mycam.devicemgmt.GetDeviceInformation()
        return resp.HardwareId

    def resolutions_available(self) -> List:
        """Find all resolutions of camera.

        Returns:
            tuple: List of resolutions (Width, Height).
        """
        request = self._camera_media.create_type('GetVideoEncoderConfigurationOptions')
        request.ProfileToken = self._camera_media_profile[0].token
        config = self._camera_media.GetVideoEncoderConfigurationOptions(request)
        # print(config)
        return [(res.Width, res.Height) for res in config.H264.ResolutionsAvailable]

    def frame_rate_range(self) -> int:
        """Find the frame rate range of camera.

        Returns:
            int: FPS min.
            int: FPS max.
        """
        request = self._camera_media.create_type('GetVideoEncoderConfigurationOptions')
        request.ProfileToken = self._camera_media_profile[0].token
        config = self._camera_media.GetVideoEncoderConfigurationOptions(request)
        return config.H264.FrameRateRange.Min, config.H264.FrameRateRange.Max
    
    def qualityRange(self) -> int:
        """Find the frame rate range of camera.

        Returns:
            int: FPS min.
            int: FPS max.
        """
        request = self._camera_media.create_type('GetVideoEncoderConfigurationOptions')
        request.ProfileToken = self._camera_media_profile[0].token
        config = self._camera_media.GetVideoEncoderConfigurationOptions(request)
        return config.QualityRange.Min, config.QualityRange.Max

    def gov_length_range(self):
        request = self._camera_media.create_type('GetVideoEncoderConfigurationOptions')
        request.ProfileToken = self._camera_media_profile[0].token
        config = self._camera_media.GetVideoEncoderConfigurationOptions(request)
        # print(type(config.H264.GovLengthRange.Max))
        return config.H264.GovLengthRange.Min, config.H264.GovLengthRange.Max
    
    def H264_profile_support(self):
        request = self._camera_media.create_type('GetVideoEncoderConfigurationOptions')
        request.ProfileToken = self._camera_media_profile[0].token
        config = self._camera_media.GetVideoEncoderConfigurationOptions(request)
        # print(type(config.H264.H264ProfilesSupported[0]))
        return config.H264.H264ProfilesSupported
          
    def date(self) -> str:
        """Find date configured on camera.

        Returns:
            str: Date in string.
        """
        datetime = self._mycam.devicemgmt.GetSystemDateAndTime()
        return datetime.UTCDateTime.Time

    def time(self) -> int:
        """Find local hour configured on camera.

        Returns:
            str: Hour in string.
        """
        datetime = self._mycam.devicemgmt.GetRemoteUser()
        return datetime

    def is_ptz(self) -> bool:
        """Check if camera is PTZ or not.

        Returns:
            bool: Is PTZ or not.
        """
        resp = self._mycam.devicemgmt.GetCapabilities()
        return bool(resp.PTZ)
    
    def get_rtsp_stream(self):
        media_service = self._mycam.create_media_service()
        token = None
        profiles = media_service.GetProfiles()
        # Use the first profile and Profiles have at least one
        token = profiles[0].token
        # token = "Profile_1"
        obj = media_service.create_type('GetStreamUri')
        obj.ProfileToken = token
        obj.StreamSetup = {'Stream': 'RTP-Unicast', 'Transport': {'Protocol': 'RTSP'}}
        # print(media_service.GetStreamUri(obj)["Uri"])
        return media_service.GetStreamUri(obj)["Uri"]
    
    def setting_now(self):
        # Create the media service
        media_service = self._mycam.create_media_service()

        profiles = media_service.GetProfiles()

        # Use the first profile and Profiles have at least one
        token = profiles[0].token

        # Get all video encoder configurations
        configurations_list = media_service.GetVideoEncoderConfigurations()

        # Use the first profile and Profiles have at least one
        video_encoder_configuration = configurations_list[0]
        print(video_encoder_configuration)        
        
    # Cài đặt chất lượng cho camera
    def set_max_setting_camera(self):
        # Create the media service
        media_service = self._mycam.create_media_service()

        profiles = media_service.GetProfiles()

        # Use the first profile and Profiles have at least one
        token = profiles[0].token

        # Get all video encoder configurations
        configurations_list = media_service.GetVideoEncoderConfigurations()

        # Use the first profile and Profiles have at least one
        video_encoder_configuration = configurations_list[0]

        # Get video encoder configuration options
        options = media_service.GetVideoEncoderConfigurationOptions({'ProfileToken':token})
        # print(options)

        # Setup stream configuration
        video_encoder_configuration.Encoding = 'H264'
        # Cài đặt độ phân giải 1920*1080
        video_encoder_configuration.Resolution.Width = \
                        options.H264.ResolutionsAvailable[0].Width
        video_encoder_configuration.Resolution.Height = \
                        options.H264.ResolutionsAvailable[0].Height
        # Cài đặt chất lượng Min-Max
        video_encoder_configuration.Quality = options.QualityRange.Max
        # FPS Min-Max
        video_encoder_configuration.RateControl.FrameRateLimit = \
                                        options.H264.FrameRateRange.Max
        # Setup EncodingInterval
        video_encoder_configuration.RateControl.EncodingInterval = \
                                        options.H264.EncodingIntervalRange.Max
        # Setup Bitrate
        # video_encoder_configuration.RateControl.BitrateLimit = \
                                # options.Extension.H264[0].BitrateRange[0].Min[0]
        # print(video_encoder_configuration)
        # Create request type instance
        request = media_service.create_type('SetVideoEncoderConfiguration')
        request.Configuration = video_encoder_configuration
        # ForcePersistence is obsolete and should always be assumed to be True
        request.ForcePersistence = True

        # Set the video encoder configuration
        media_service.SetVideoEncoderConfiguration(request)
        
    def apply_new_setting(self, width, height, fps, quality, H264_profile, GOV_length):
        # Create the media service
        media_service = self._mycam.create_media_service()

        profiles = media_service.GetProfiles()

        # Use the first profile and Profiles have at least one
        token = profiles[0].token

        # Get all video encoder configurations
        configurations_list = media_service.GetVideoEncoderConfigurations()

        # Use the first profile and Profiles have at least one
        video_encoder_configuration = configurations_list[0]

        # Get video encoder configuration options
        options = media_service.GetVideoEncoderConfigurationOptions({'ProfileToken':token})

        # Setup stream configuration
        video_encoder_configuration.Encoding = 'H264'
        # Cài đặt độ phân giải 1920*1080
        video_encoder_configuration.Resolution.Width = width
        video_encoder_configuration.Resolution.Height = height
        # Cài đặt chất lượng Min-Max
        video_encoder_configuration.Quality = quality
        # FPS Min-Max
        video_encoder_configuration.RateControl.FrameRateLimit = fps
        # Setup EncodingInterval
        video_encoder_configuration.RateControl.EncodingInterval = options.H264.EncodingIntervalRange.Max
        # Setup GOV
        video_encoder_configuration.H264.GovLength = GOV_length
        #Set up H264
        video_encoder_configuration.H264.H264Profile = H264_profile
        # Setup Bitrate
        # video_encoder_configuration.RateControl.BitrateLimit = \
                                # options.Extension.H264[0].BitrateRange[0].Min[0]
        # print(video_encoder_configuration)
        # Create request type instance
        request = media_service.create_type('SetVideoEncoderConfiguration')
        request.Configuration = video_encoder_configuration
        # ForcePersistence is obsolete and should always be assumed to be True
        request.ForcePersistence = True

        # Set the video encoder configuration
        media_service.SetVideoEncoderConfiguration(request)    
    
if __name__ == "__main__":
    camera = Camera(ip= "169.254.184.113", user= "", password="")
    # print(camera.model())
    # full_hd = camera.resolutions_available()
    # print(full_hd[0][1])
    # camera.get_rtsp_stream()
    # print(camera.qualityRange())
    # print(camera.detail_video())
    # camera.resolutions_available()
    # camera.setting_now()
    # camera.media_profile_configuration()
    print(camera.H264_profile_support())
    # camera.apply_new_setting(width =1280 , height=720 , fps= 20 , quality= 40, H264_profile= 'High', GOV_length= 30)