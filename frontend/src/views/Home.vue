<template>
  <div class="home">
    <div class="hero">
      <h1 class="title">AI 智能客服系统</h1>
      <p class="subtitle">基于 RAG 技术的智能问答解决方案</p>
      <div class="actions">
        <el-button type="primary" size="large" @click="$router.push('/chat')">
          <el-icon><ChatDotRound /></el-icon>
          开始对话
        </el-button>
        <el-button size="large" @click="$router.push('/admin')">
          <el-icon><Setting /></el-icon>
          知识库管理
        </el-button>
      </div>
    </div>

    <div class="features">
      <h2 class="section-title">核心功能</h2>
      <el-row :gutter="20">
        <el-col :span="8">
          <div class="feature-card">
            <div class="feature-icon">
              <el-icon size="48" color="#409EFF"><Document /></el-icon>
            </div>
            <h3>文档智能解析</h3>
            <p>支持 PDF、Word、TXT 等多种格式文档上传和自动解析</p>
          </div>
        </el-col>
        <el-col :span="8">
          <div class="feature-card">
            <div class="feature-icon">
              <el-icon size="48" color="#67C23A"><Search /></el-icon>
            </div>
            <h3>RAG 检索增强</h3>
            <p>基于向量数据库的智能检索，精准定位相关知识</p>
          </div>
        </el-col>
        <el-col :span="8">
          <div class="feature-card">
            <div class="feature-icon">
              <el-icon size="48" color="#E6A23C"><ChatDotRound /></el-icon>
            </div>
            <h3>智能对话</h3>
            <p>支持多轮对话，上下文理解，提供专业准确的回答</p>
          </div>
        </el-col>
      </el-row>
    </div>

    <div class="tech-stack">
      <h2 class="section-title">技术栈</h2>
      <div class="tech-tags">
        <el-tag size="large" effect="dark">Vue 3</el-tag>
        <el-tag size="large" effect="dark" type="success">FastAPI</el-tag>
        <el-tag size="large" effect="dark" type="warning">ChromaDB</el-tag>
        <el-tag size="large" effect="dark" type="danger">智谱 AI</el-tag>
        <el-tag size="large" effect="dark" type="info">RAG</el-tag>
      </div>
    </div>
  </div>
</template>

<style scoped>
.home {
  padding: 40px 0;
}

.hero {
  text-align: center;
  padding: 60px 0;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 16px;
  color: white;
  margin-bottom: 60px;
}

.title {
  font-size: 48px;
  font-weight: 700;
  margin-bottom: 16px;
}

.subtitle {
  font-size: 20px;
  opacity: 0.9;
  margin-bottom: 32px;
}

.actions {
  display: flex;
  gap: 16px;
  justify-content: center;
}

.actions .el-button {
  padding: 16px 32px;
  font-size: 16px;
}

.features {
  margin-bottom: 60px;
}

.section-title {
  text-align: center;
  font-size: 32px;
  font-weight: 600;
  margin-bottom: 40px;
  color: #303133;
}

.feature-card {
  background: white;
  padding: 40px 30px;
  border-radius: 12px;
  text-align: center;
  box-shadow: 0 4px 20px rgba(0,0,0,0.08);
  transition: transform 0.3s;
}

.feature-card:hover {
  transform: translateY(-4px);
}

.feature-icon {
  margin-bottom: 20px;
}

.feature-card h3 {
  font-size: 20px;
  font-weight: 600;
  margin-bottom: 12px;
  color: #303133;
}

.feature-card p {
  color: #606266;
  line-height: 1.6;
}

.tech-stack {
  text-align: center;
  padding: 40px 0;
}

.tech-tags {
  display: flex;
  gap: 16px;
  justify-content: center;
  flex-wrap: wrap;
}

.tech-tags .el-tag {
  padding: 12px 24px;
  font-size: 16px;
}
</style>
