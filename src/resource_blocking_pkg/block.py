BLOCK_RESOURCE_TYPES = [
  'beacon',
  'csp_report',
  'font',
  'image',
  'imageset',
  'media',
  'object',
  'texttrack',
#  we can even block stylsheets and scripts though it's not recommended:
# 'stylesheet',
# 'script',  
# 'xhr',
]


# we can also block popular 3rd party resources like tracking and advertisements.
BLOCK_RESOURCE_NAMES = [
  'adzerk',
  'analytics',
  'cdn.api.twitter',
  'doubleclick',
  'exelator',
  'facebook',
  'fontawesome',
  #'google',
  'google-analytics',
  'googletagmanager',
]

def intercept_route(route):
    """intercept all requests and abort blocked ones"""
    if route.request.resource_type in BLOCK_RESOURCE_TYPES:
        print(f'blocking background resource {route.request} blocked type "{route.request.resource_type}"')
        return route.abort()
    if any(key in route.request.url for key in BLOCK_RESOURCE_NAMES):
        print(f"blocking background resource {route.request} blocked name {route.request.url}")
        return route.abort()
    return route.continue_()


if __name__ == "__main__":
  intercept_route()