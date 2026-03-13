"""
快速测试脚本
测试系统各模块是否正常工作
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app import app
from models import db, Novel, Chapter, Character
from services.ai_service import AIService

def test_database():
    """测试数据库"""
    print("\n=== 测试数据库 ===")
    with app.app_context():
        novels = Novel.query.all()
        print(f"✅ 数据库连接成功")
        print(f"   - 小说数量: {len(novels)}")
        for novel in novels:
            print(f"   - {novel.title}")
    return True

def test_api():
    """测试 API 接口"""
    print("\n=== 测试 API 接口 ===")
    client = app.test_client()
    
    # 测试健康检查
    response = client.get('/api/health')
    if response.status_code == 200:
        print("✅ API 服务正常")
    else:
        print("❌ API 服务异常")
        return False
    
    # 测试小说列表
    response = client.get('/api/novels/')
    if response.status_code == 200:
        data = response.get_json()
        print(f"✅ 小说列表接口正常，共 {len(data.get('data', []))} 部小说")
    else:
        print("❌ 小说列表接口异常")
        return False
    
    return True

def test_ai_service():
    """测试 AI 服务"""
    print("\n=== 测试 AI 服务 ===")
    
    # 检查 API Key
    from config.settings import config
    if not config.AI_API_KEY or config.AI_API_KEY == 'your-deepseek-api-key-here':
        print("⚠️  未配置 AI_API_KEY，跳过测试")
        print("   请在 backend/.env 文件中配置你的 DeepSeek API Key")
        return False
    
    print("✅ AI API Key 已配置")
    print(f"   - 模型: {config.AI_MODEL}")
    print(f"   - API Base: {config.AI_API_BASE}")
    
    return True

def run_all_tests():
    """运行所有测试"""
    print("=" * 50)
    print("  AI 小说自动化系统 - 测试套件")
    print("=" * 50)
    
    tests = [
        ("数据库", test_database),
        ("API 接口", test_api),
        ("AI 服务", test_ai_service)
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ {name} 测试失败: {str(e)}")
            results.append((name, False))
    
    print("\n" + "=" * 50)
    print("  测试结果汇总")
    print("=" * 50)
    for name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{name}: {status}")
    
    all_passed = all(result for _, result in results)
    if all_passed:
        print("\n🎉 所有测试通过！系统已准备就绪。")
    else:
        print("\n⚠️  部分测试未通过，请检查配置。")
    
    return all_passed


if __name__ == '__main__':
    run_all_tests()
