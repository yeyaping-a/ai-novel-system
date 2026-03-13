import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import axios from 'axios'

const API_BASE = 'http://localhost:5000/api'

function ChapterEditor() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [chapter, setChapter] = useState(null)
  const [content, setContent] = useState('')
  const [generating, setGenerating] = useState(false)

  useEffect(() => {
    loadChapter()
  }, [id])

  const loadChapter = async () => {
    try {
      const res = await axios.get(`${API_BASE}/chapters/${id}`)
      setChapter(res.data.data)
      setContent(res.data.data.content || '')
    } catch (error) {
      console.error('加载章节失败:', error)
    }
  }

  const saveChapter = async () => {
    try {
      await axios.put(`${API_BASE}/chapters/${id}`, { content })
      alert('保存成功！')
      loadChapter()
    } catch (error) {
      alert('保存失败: ' + (error.response?.data?.message || error.message))
    }
  }

  const generateContent = async () => {
    setGenerating(true)
    try {
      const res = await axios.post(`${API_BASE}/generate/chapter/${id}`)
      setContent(res.data.data.content || '')
      alert('生成成功！')
      loadChapter()
    } catch (error) {
      alert('生成失败: ' + (error.response?.data?.message || error.message))
    } finally {
      setGenerating(false)
    }
  }

  const polishContent = async () => {
    setGenerating(true)
    try {
      const res = await axios.post(`${API_BASE}/generate/polish/${id}`)
      setContent(res.data.data.polished)
      alert('润色完成，请查看并确认')
    } catch (error) {
      alert('润色失败: ' + (error.response?.data?.message || error.message))
    } finally {
      setGenerating(false)
    }
  }

  if (!chapter) {
    return <div className="text-center py-10">加载中...</div>
  }

  return (
    <div className="space-y-4">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold">
            第{chapter.chapter_number}章 {chapter.title}
          </h1>
          <p className="text-gray-600">
            {content.length} 字 · {chapter.status}
          </p>
        </div>
        <div className="flex space-x-2">
          <button
            onClick={generateContent}
            disabled={generating}
            className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 disabled:opacity-50"
          >
            {generating ? '生成中...' : 'AI 生成'}
          </button>
          <button
            onClick={polishContent}
            disabled={generating || !content}
            className="bg-purple-500 text-white px-4 py-2 rounded hover:bg-purple-600 disabled:opacity-50"
          >
            AI 润色
          </button>
          <button
            onClick={saveChapter}
            className="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600"
          >
            保存
          </button>
        </div>
      </div>

      <div className="bg-white rounded-lg shadow">
        <textarea
          value={content}
          onChange={(e) => setContent(e.target.value)}
          className="w-full h-[600px] p-6 border-none outline-none resize-none font-serif text-lg leading-relaxed"
          placeholder="在这里输入章节内容..."
        />
      </div>
    </div>
  )
}

export default ChapterEditor
