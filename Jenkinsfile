pipeline {
  environment {
    Image_name = "deepdockerpro/converse"
    DockerHubCredential = 'deepdockerpro-dockerhub'
    Docker_image = ''
  }
  agent any
  stages {
    stage('Cloning Git') {
      steps {
        git([url: 'https://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@github.com/deeplearn-optimizer/converse.git', branch: 'master', credentialsId: 'deepdockerpro-github'])

      }
    }
    stage('Build Python Application') {
	steps{
         sh "python3 manage.py migrate"
      }
    }
    stage('Test Python Application') {
      steps{
         sh "python3 manage.py test"
      }
    }
    stage('Build Docker Image') {
      steps{
        script {
          Docker_image = docker.build Image_name
        }
      }
    }
    stage('Deploy Image to Docker Hub') {
      steps{
        script {
          docker.withRegistry( '', DockerHubCredential ) {
             Docker_image.push('latest')
          }
        }
      }
    }
    stage('Delete Docker Image') {
      steps{
         sh "docker rmi $Image_name:latest"
      }
    }

    stage("Run Ansible Playbook") {
      steps{
      ansiblePlaybook(
      	credentialsId: "container_access_key",
        inventory: "Inventory",
        installation: "ansible",
        limit: "",
        playbook: "docker_playbook.yaml",
        extras: ""
      )
    }
    }

  }
}
