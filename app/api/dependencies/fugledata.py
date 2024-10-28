import fugledata


def get_fugle_data(base_url):
    configuration = fugledata.Configuration(
        host=base_url
    )
    return fugledata.ApiClient(configuration)