import git
from datetime import datetime, timedelta

class GitAnalyzer:
    def __init__(self, repo_path):
        self.repo = git.Repo(repo_path)

    def get_recently_changed_files(self, days=7):
        """
        Get a list of files that have been changed in the last `days`.
        """
        since_date = datetime.now() - timedelta(days=days)
        commits = self.repo.iter_commits(since=since_date.isoformat())
        changed_files = set()
        for commit in commits:
            for file in commit.stats.files:
                changed_files.add(file)
        return list(changed_files)

    def get_files_related_to_commit(self, commit_hash):
        """
        Get a list of files related to a specific commit.
        """
        commit = self.repo.commit(commit_hash)
        return list(commit.stats.files.keys())
