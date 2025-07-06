pipeline {
  agent any

  stages {
    stage('Trigger Auto PR Pipeline') {
      steps {
        build job: 'auto-pr-pipeline', parameters: [
          string(name: 'GITHUB_USER', value: 'dorado-ai-devops'),
          string(name: 'GITHUB_REPO', value: 'ai-helm-linter')
        ]
      }
    }
  }
}
