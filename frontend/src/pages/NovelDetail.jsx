import { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import axios from 'axios'

const API_BASE = 'http://localhost:5000/api'

function NovelDetail() {
  const { id } = useParams()
  const [novel, setNovel] = useState(null)
  const [chapters, setChapters] = useState([])
  const [activeTab, setActiveTab] = useState('chapters')

  useEffect(() => {
    loadNovel()
    loadChapters()
  }, [id])

  const loadNovel = async () => {
    try {
      const res = await axios.get(`${API_BASE}/novels/${id}`)
      setNovel(res.data.data)
    } catch (error) {
      console.error('加载小说详情失败:', error)
    }
  }

  const loadChapters = async () => {
    try {
      const res = await axios.get(`${API_BASE}/chapters/?novel_id=${id}`)
      setChapters(res.data.data)
    } catch (error) {
      console.error('加载章节列表失败:', error)
    }
  }

  const generateChapter = async (chapterId) => {
    try {
      const res = await axios.post(`${API_BASE}/generate/chapter/${chapterId}`)
      alert('章节生成成功！')
      loadChapters()
    } catch (error) {
      alert('生成失败: ' + (error.response?.data?.message || error.message))
    }
  }

  if (!novel) {
    return <div className="text-center py-10">加载中...</div>
  }

  return (
    <div className="space-y-6">
      {/* 小说信息 */}
      <div className="bg-white rounded-lg shadow p-6">
        <div className="flex justify-between items-start mb-4">
          <div>
            <h1 className="text-2xl font-bold mb-2">{novel.title}</h1>
            <p className="text-gray-600">{novel.genre} · {novel.author}</p>
          </div>
          <Link
            to={`/reader/${id}`}
            className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
          >
            开始阅读
          </Link>
        </div>

        <div className="grid grid-cols-3 gap-4 text-center border-t pt-4">
          <div>
            <div className="text-2xl font-bold">{novel.total_chapters}</div>
            <div className="text-sm text-gray-500">章节</div>
          </div>
          <div>
            <div className="text-2xl font-bold">{novel.total_words.toLocaleString()}</div>
            <div className="text-sm text-gray-500">字数</div>
          </div>
          <div>
            <div className="text-2xl font-bold">{chapters.filter(c => c.status === 'published').length}</div>
            <div className="text-sm text-gray-500">已发布</div>
          </div>
        </div>
      </div>

      {/* 标签页 */}
      <div className="bg-white rounded-lg shadow">
        <div className="border-b">
          <div className="flex">
            <button
              onClick={() => setActiveTab('chapters')}
              className={`px-6 py-3 font-medium ${
                activeTab === 'chapters'
                  ? 'text-blue-500 border-b-2 border-blue-500'
                  : 'text-gray-600'
              }`}
            >
              章节管理
            </button>
            <button
              onClick={() => setActiveTab('settings')}
              className={`px-6 py-3 font-medium ${
                activeTab === 'settings'
                  ? 'text-blue-500 border-b-2 border-blue-500'
                  : 'text-gray-600'
              }`}
            >
              世界观设定
            </button>
            <button
              onClick={() => setActiveTab('characters')}
              className={`px-6 py-3 font-medium ${
                activeTab === 'characters'
                  ? 'text-blue-500 border-b-2 border-blue-500'
                  : 'text-gray-600'
              }`}
            >
              人物设定
            </button>
          </div>
        </div>

        <div className="p-6">
          {activeTab === 'chapters' && (
            <div className="space-y-4">
              <div className="flex justify-between items-center">
                <h3 className="font-bold">章节列表</h3>
                <button className="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600">
                  批量生成大纲
                </button>
              </div>

              {chapters.length === 0 ? (
                <div className="text-center py-10 text-gray-500">
                  还没有章节，点击上方按钮开始创作
                </div>
              ) : (
                <div className="space-y-2">
                  {chapters.map(chapter => (
                    <div
                      key={chapter.id}
                      className="flex justify-between items-center p-4 bg-gray-50 rounded hover:bg-gray-100"
                    >
                      <div>
                        <div className="font-medium">
                          第{chapter.chapter_number}章 {chapter.title}
                        </div>
                        <div className="text-sm text-gray-500">
                          {chapter.word_count} 字 · 
                          <span className={`ml-2 ${
                            chapter.status === 'published' ? 'text-green-500' :
                            chapter.status === 'generated' ? 'text-blue-500' : 'text-gray-400'
                          }`}>
                            {chapter.status === 'published' ? '已发布' :
                             chapter.status === 'generated' ? '已生成' : '草稿'}
                          </span>
                        </div>
                      </div>
                      <div className="flex space-x-2">
                        {chapter.status === 'draft' && (
                          <button
                            onClick={() => generateChapter(chapter.id)}
                            className="bg-blue-500 text-white px-3 py-1 rounded text-sm hover:bg-blue-600"
                          >
                            AI生成
                          </button>
                        )}
                        <Link
                          to={`/chapters/${chapter.id}/edit`}
                          className="bg-gray-500 text-white px-3 py-1 rounded text-sm hover:bg-gray-600"
                        >
                          编辑
                        </Link>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {activeTab === 'settings' && (
            <div className="space-y-4">
              <h3 className="font-bold">世界观设定</h3>
              <div className="bg-gray-50 p-4 rounded whitespace-pre-wrap">
                {novel.world_setting || '暂无设定'}
              </div>
            </div>
          )}

          {activeTab === 'characters' && (
            <div className="space-y-4">
              <h3 className="font-bold">人物设定</h3>
              {novel.characters && novel.characters.length > 0 ? (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {novel.characters.map(char => (
                    <div key={char.id} className="bg-gray-50 p-4 rounded">
                      <div className="font-bold text-lg">{char.name}</div>
                      <div className="text-sm text-gray-600 mb-2">
                        {char.role === 'protagonist' ? '主角' :
                         char.role === 'antagonist' ? '反派' : '配角'} · 
                        {char.occupation}
                      </div>
                      <div className="text-sm">{char.personality}</div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="text-center py-10 text-gray-500">
                  暂无人物设定
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default NovelDetail
