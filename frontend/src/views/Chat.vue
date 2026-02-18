<template>
  <div class="chat-page">
    <div class="chat-container">
      <div class="chat-header">
        <h2>
          <el-icon><ChatDotRound /></el-icon>
          智能客服对话
        </h2>
        <el-button type="danger" text @click="clearChat">
          <el-icon><Delete /></el-icon>
          清空对话
        </el-button>
      </div>

      <div class="chat-messages" ref="messagesContainer">
        <div v-if="messages.length === 0" class="empty-state">
          <el-icon size="64" color="#dcdfe6"><ChatLineRound /></el-icon>
          <p>开始你的第一次对话吧</p>
          <div class="quick-questions">
            <el-button
              v-for="q in quickQuestions"
              :key="q"
              type="primary"
              plain
              @click="sendQuickQuestion(q)"
            >
              {{ q }}
            </el-button>
          </div>
        </div>

        <div
          v-for="(msg, index) in messages"
          :key="index"
          :class="['message', msg.role]"
        >
          <div class="message-avatar">
            <el-icon v-if="msg.role === 'user'" size="24"><User /></el-icon>
            <el-icon v-else size="24" color="#409EFF"><Service /></el-icon>
          </div>
          <div class="message-content">
            <div class="message-text" v-html="formatMessage(msg.content)"></div>
            <div v-if="msg.sources && msg.sources.length" class="message-sources">
              <el-tag size="small" type="info">引用 {{ msg.sources.length }} 个来源</el-tag>
            </div>
          </div>
        </div>

        <div v-if="loading" class="message assistant loading">
          <div class="message-avatar">
            <el-icon size="24" color="#409EFF"><Service /></el-icon>
          </div>
          <div class="message-content">
            <el-skeleton :rows="2" animated />
          </div>
        </div>
      </div>

      <div class="chat-input">
        <el-input
          v-model="inputMessage"
          type="textarea"
          :rows="3"
          placeholder="输入你的问题..."
          @keydown.enter.prevent="sendMessage"
        />
        <el-button
          type="primary"
          :loading="loading"
          :disabled="!inputMessage.trim()"
          @click="sendMessage"
        >
          <el-icon><Promotion /></el-icon>
          发送
        </el-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick, onMounted } from 'vue'
import { ElMessage } from 'element-plus'

const messages = ref([])
const inputMessage = ref('')
const loading = ref(false)
const messagesContainer = ref(null)
const error = ref('')

const quickQuestions = [
  '你们的产品有哪些功能？',
  '如何联系客服？',
  '产品价格是多少？',
  '支持哪些支付方式？'
]

const formatMessage = (text) => {
  return text.replace(/\n/g, '<br>')
}

const scrollToBottom = () => {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
  })
}

const sendQuickQuestion = (q) => {
  inputMessage.value = q
  sendMessage()
}

// 调用后端 API
const sendMessage = async () => {
  if (!inputMessage.value.trim() || loading.value) return

  const userMessage = inputMessage.value.trim()
  messages.value.push({
    role: 'user',
    content: userMessage
  })

  inputMessage.value = ''
  loading.value = true
  error.value = ''
  scrollToBottom()

  try {
    const response = await fetch('/api/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        message: userMessage,
        history: messages.value
      })
    })

    if (!response.ok) {
      throw new Error('请求失败')
    }

    const result = await response.json()
    
    messages.value.push({
      role: 'assistant',
      content: result.answer,
      sources: result.sources
    })
  } catch (err) {
    error.value = '请求失败，使用本地知识库回答'
    // 如果后端不可用，使用本地知识库
    const answer = findAnswerLocal(userMessage)
    messages.value.push({
      role: 'assistant',
      content: answer,
      sources: ['本地知识库']
    })
  } finally {
    loading.value = false
    scrollToBottom()
  }
}

// 本地知识库（备用）
const findAnswerLocal = (question) => {
  const knowledgeBase = [
    {
      keywords: ['功能', '产品', '做什么'],
      answer: '我们的AI智能客服系统主要功能包括：\n\n1. **文档智能解析** - 支持PDF、Word、TXT等多种格式文档上传和自动解析\n2. **RAG检索增强** - 基于向量数据库的智能检索，精准定位相关知识\n3. **智能对话** - 支持多轮对话，上下文理解，提供专业准确的回答\n4. **知识库管理** - 便捷的知识库管理界面，支持文档增删改查'
    },
    {
      keywords: ['联系', '客服', '电话', '邮箱'],
      answer: '您可以通过以下方式联系我们：\n\n- **邮箱**：w2587913928@163.com\n- **开发者**：吴叶龙\n- **项目地址**：https://github.com/2587958021/AI-CustomerService\n\n我们会在24小时内回复您的问题。'
    },
    {
      keywords: ['价格', '多少钱', '费用'],
      answer: '目前我们的AI智能客服系统提供以下方案：\n\n- **免费版**：基础功能，适合个人和小团队使用\n- **专业版**：更多功能和更高配额，适合中小企业\n- **企业版**：定制化解决方案，适合大型企业\n\n具体价格请咨询我们的销售团队。'
    },
    {
      keywords: ['支付', '付款', '方式'],
      answer: '我们支持多种支付方式：\n\n- 支付宝\n- 微信支付\n- 银行转账\n- 对公账户\n\n企业用户还可以选择月付或年付，年付可享受8折优惠。'
    },
    {
      keywords: ['技术', '技术栈', '原理'],
      answer: '我们的系统采用业界领先的技术栈：\n\n**前端**：Vue 3 + Element Plus\n**后端**：FastAPI + Python\n**向量数据库**：ChromaDB\n**大模型**：智谱AI GLM-4\n**文档解析**：PyPDF2、python-docx\n\n基于RAG（检索增强生成）技术，确保回答准确可靠。'
    }
  ]

  const q = question.toLowerCase()
  for (const item of knowledgeBase) {
    for (const keyword of item.keywords) {
      if (q.includes(keyword.toLowerCase())) {
        return item.answer
      }
    }
  }
  
  return '感谢您的提问！这个问题我需要更多信息才能回答。\n\n您可以尝试询问以下问题：\n- 产品有哪些功能？\n- 如何联系客服？\n- 产品价格是多少？\n- 支持哪些支付方式？\n- 技术栈是什么？'
}

const clearChat = async () => {
  messages.value = []
  
  // 调用后端清空历史
  try {
    await fetch('/api/chat/history', { method: 'DELETE' })
  } catch (err) {
    console.log('清空历史失败', err)
  }
}

// 加载历史记录
onMounted(async () => {
  try {
    const response = await fetch('/api/chat/history')
    if (response.ok) {
      const history = await response.json()
      // 只显示最近20条
      messages.value = history.slice(-20).map(h => ({
        role: h.role,
        content: h.content,
        sources: h.sources
      }))
    }
  } catch (err) {
    console.log('加载历史记录失败', err)
  }
})
</script>

<style scoped>
.chat-page {
  height: calc(100vh - 140px);
}

.chat-container {
  display: flex;
  flex-direction: column;
  height: 100%;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.08);
  overflow: hidden;
}

.chat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 24px;
  border-bottom: 1px solid #e4e7ed;
}

.chat-header h2 {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 18px;
  font-weight: 600;
  color: #303133;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #909399;
}

.empty-state p {
  margin: 16px 0;
  font-size: 16px;
}

.quick-questions {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  justify-content: center;
  margin-top: 24px;
}

.message {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
}

.message.user {
  flex-direction: row-reverse;
}

.message-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: #f5f7fa;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.message.user .message-avatar {
  background: #409EFF;
  color: white;
}

.message-content {
  max-width: 70%;
  padding: 12px 16px;
  border-radius: 12px;
  background: #f5f7fa;
}

.message.user .message-content {
  background: #409EFF;
  color: white;
}

.message-text {
  line-height: 1.6;
  word-break: break-word;
}

.message-sources {
  margin-top: 8px;
}

.chat-input {
  display: flex;
  gap: 12px;
  padding: 16px 24px;
  border-top: 1px solid #e4e7ed;
  background: #fafafa;
}

.chat-input .el-textarea {
  flex: 1;
}

.chat-input .el-button {
  align-self: flex-end;
  padding: 12px 24px;
}
</style>
