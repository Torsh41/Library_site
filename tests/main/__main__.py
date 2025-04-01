from . import main_
from .. import get_application

if __name__ == "__main__":
    app = get_application()
    main_(app)
