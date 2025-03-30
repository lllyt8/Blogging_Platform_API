from app.db.session import engine
from app.db.base import Base
from app.models import user, post  # 导入所有模型
from app.crud import user as crud_user

def init_db():
    # 创建所有表
    Base.metadata.create_all(bind=engine)

def init_test_data(db):
    # 创建测试数据
    test_user = crud_user.create_user(
        db=db,
        name="测试用户",
        email="test@example.com",
        age=25
    )