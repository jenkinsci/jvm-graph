def jobProperties = [
  buildDiscarder(logRotator(numToKeepStr: '50', artifactNumToKeepStr: '50')),
  disableConcurrentBuilds(abortPrevious: true)
]

if (env.BRANCH_IS_PRIMARY) {
  // Run at least weekly on the primary branch
  jobProperties << pipelineTriggers([cron('@weekly')])
}

properties(jobProperties)

node('linux-21') {
  timeout(time: 5, unit: 'MINUTES') {
    stage('Checkout') {
      checkout scm
    }

    stage('Build') {
      sh '''
          python3 -m venv venv
          . venv/bin/activate
          pip install -U pip setuptools
          pip install -r requirements.txt
          python jvm-graph.py
          deactivate
          '''.stripIndent()
    }

    stage('Archive') {
      archiveArtifacts 'jvm-graph.png'
    }
  }
}

