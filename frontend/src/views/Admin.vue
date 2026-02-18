<template>
  <div class="admin-page">
    <h2 class="page-title">
      <el-icon><Setting /></el-icon>
      知识库管理
    </h2>

    <div class="upload-section">
      <el-card>
        <template #header>
          <div class="card-header">
            <span>上传文档</span>
          </div>
        </template>
        <el-upload
          class="upload-demo"
          drag
          action="#"
          :auto-upload="false"
          :on-change="handleFileChange"
          accept=".pdf,.docx,.txt"
        >
          <el-icon class="el-icon--upload" size="64"><UploadFilled /></el-icon>
          <div class="el-upload__text">
            拖拽文件到此处或 <em>点击上传</em>
          </div>
          <template #tip>
            <div class="el-upload__tip">
              支持 PDF、Word、TXT 格式，单个文件不超过 10MB
            </div>
          </template>
        </el-upload>
        <div v-if="uploading" class="upload-progress">
          <el-progress :percentage="uploadProgress" />
        </div>
      </el-card>
    </div>

    <div class="documents-section">
      <el-card>
        <template #header>
          <div class="card-header">
            <span>文档列表</span>
            <el-tag type="info">{{ documents.length }} 个文档</el-tag>
          </div>
        </template>
        <el-table :data="documents" style="width: 100%">
          <el-table-column prop="filename" label="文件名" />
          <el-table-column prop="chunks_count" label="分段数" width="100" />
          <el-table-column prop="createdAt" label="上传时间" width="180" />
          <el-table-column label="操作" width="120">
            <template #default="scope">
              <el-button
                type="danger"
                text
                size="small"
                @click="deleteDocument(scope.row)"
              >
                <el-icon><Delete /></el-icon>
                删除
              </el-button>
            </template>
          </el-table-column>
        </el-table>
        <el-empty v-if="documents.length === 0" description="暂无文档" />
      </el-card>
    </div>

    <div class="knowledge-section">
      <el-card>
        <template #header>
          <div class="card-header">
            <span>知识库内容</span>
            <el-tag type="success">{{ knowledgeItems.length }} 条知识</el-tag>
          </div>
        </template>
        <el-collapse>
          <el-collapse-item
            v-for="(item, index) in knowledgeItems"
            :key="index"
            :title="item.keywords.join(' / ')"
          >
            <div class="knowledge-content">{{ item.answer }}</div>
          </el-collapse-item>
        </el-collapse>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'

const documents = ref([
  {
    id: '1',
    filename: '产品功能介绍.pdf',
    chunks_count: 5,
    createdAt: '2025-02-18 10:30'
  },
  {
    id: '2',
    filename: '价格方案.docx',
    chunks_count: 3,
    createdAt: '2025-02-18 11:15'
  },
  {
    id: '3',
    filename: '技术文档.txt',
    chunks_count: 8,
    createdAt: '2025-02-18 14:20'
  }
])

const knowledgeItems = ref([
  {
    keywords: ['功能', '产品', '做什么'],
    answer: '我们的AI智能客服系统主要功能包括：文档智能解析、RAG检索增强、智能对话、知识库管理。'
  },
  {
    keywords: ['联系', '客服', '电话', '邮箱'],
    answer: '邮箱：w2587913928@163.com，开发者：吴叶龙。'
  },
  {
    keywords: ['价格', '多少钱', '费用'],
    answer: '提供免费版、专业版、企业版三种方案。'
  },
  {
    keywords: ['支付', '付款', '方式'],
    answer: '支持支付宝、微信支付、银行转账、对公账户。'
  },
  {
    keywords: ['技术', '技术栈', '原理'],
    answer: '前端：Vue 3 + Element Plus，后端：FastAPI + Python，向量数据库：ChromaDB，大模型：智谱AI GLM-4。'
  }
])

const uploading = ref(false)
const uploadProgress = ref(0)

const handleFileChange = (file) => {
  uploading.value = true
  uploadProgress.value = 0
  
  // 模拟上传进度
  const interval = setInterval(() => {
    uploadProgress.value += 20
    if (uploadProgress.value >= 100) {
      clearInterval(interval)
      uploading.value = false
      
      // 添加文档到列表
      documents.value.push({
        id: String(documents.value.length + 1),
        filename: file.name,
        chunks_count: Math.floor(Math.random() * 10) + 1,
        createdAt: new Date().toLocaleString()
      })
      
      ElMessage.success('上传成功')
    }
  }, 200)
}

const deleteDocument = async (doc) => {
  try {
    await ElMessageBox.confirm('确定要删除该文档吗？', '提示', {
      type: 'warning'
    })
    
    const index = documents.value.findIndex(d => d.id === doc.id)
    if (index > -1) {
      documents.value.splice(index, 1)
    }
    
    ElMessage.success('删除成功')
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}
</script>

<style scoped>
.admin-page {
  padding: 20px 0;
}

.page-title {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 24px;
  font-weight: 600;
  margin-bottom: 24px;
  color: #303133;
}

.upload-section {
  margin-bottom: 24px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.upload-demo {
  text-align: center;
}

.el-icon--upload {
  color: #409EFF;
  margin-bottom: 16px;
}

.el-upload__text {
  font-size: 16px;
  color: #606266;
}

.el-upload__text em {
  color: #409EFF;
  font-style: normal;
}

.el-upload__tip {
  margin-top: 16px;
  color: #909399;
}

.upload-progress {
  margin-top: 20px;
}

.documents-section {
  margin-bottom: 24px;
}

.knowledge-section {
  margin-bottom: 24px;
}

.knowledge-content {
  padding: 12px;
  background: #f5f7fa;
  border-radius: 8px;
  line-height: 1.6;
  color: #606266;
}
</style>
