from typing import List

from sqlalchemy import ARRAY, BigInteger, Boolean, CHAR, Column, DateTime, ForeignKeyConstraint, Integer, PrimaryKeyConstraint, String, Table, Text
from sqlalchemy.orm import Mapped, declarative_base, mapped_column, relationship
from sqlalchemy.orm.base import Mapped

Base = declarative_base()
metadata = Base.metadata


t_count_data_in_database = Table(
    'count_data_in_database', metadata,
    Column('repositories_count', BigInteger),
    Column('users_count', BigInteger),
    Column('issues_count', BigInteger),
    Column('pull_requests_count', BigInteger),
    Column('commits_count', BigInteger),
    Column('total_count', BigInteger),
    schema='public'
)


class UserAccount(Base):
    __tablename__ = 'user_account'
    __table_args__ = (
        PrimaryKeyConstraint('user_id', name='user_account_pkey'),
        {'schema': 'public'}
    )

    user_id = mapped_column(Integer)
    user_login = mapped_column(String(40), nullable=False)
    real_name = mapped_column(String(64))
    html_url = mapped_column(String(255), nullable=False)
    avatar_url = mapped_column(String(255))

    repository: Mapped[List['Repository']] = relationship('Repository', uselist=True, back_populates='owner')
    issue: Mapped[List['Issue']] = relationship('Issue', uselist=True, back_populates='user')
    pull_request: Mapped[List['PullRequest']] = relationship('PullRequest', uselist=True, back_populates='user')


class Repository(Base):
    __tablename__ = 'repository'
    __table_args__ = (
        ForeignKeyConstraint(['owner_id'], ['public.user_account.user_id'], name='repository_owner_id_fkey'),
        PrimaryKeyConstraint('repository_id', name='repository_pkey'),
        {'schema': 'public'}
    )

    repository_id = mapped_column(Integer)
    owner_id = mapped_column(Integer, nullable=False)
    repo_name = mapped_column(String(40), nullable=False)
    repo_full_name = mapped_column(String(100), nullable=False)
    private = mapped_column(Boolean, nullable=False)
    created_at = mapped_column(DateTime, nullable=False)
    updated_at = mapped_column(DateTime, nullable=False)
    html_url = mapped_column(String(255), nullable=False)
    description = mapped_column(Text)
    main_language = mapped_column(String(30))

    owner: Mapped['UserAccount'] = relationship('UserAccount', back_populates='repository')
    issue: Mapped[List['Issue']] = relationship('Issue', uselist=True, back_populates='repository')
    pull_request: Mapped[List['PullRequest']] = relationship('PullRequest', uselist=True, back_populates='repository')
    git_commit: Mapped[List['GitCommit']] = relationship('GitCommit', uselist=True, back_populates='repository')


class Issue(Base):
    __tablename__ = 'issue'
    __table_args__ = (
        ForeignKeyConstraint(['repository_id'], ['public.repository.repository_id'], name='issue_repository_id_fkey'),
        ForeignKeyConstraint(['user_id'], ['public.user_account.user_id'], name='issue_user_id_fkey'),
        PrimaryKeyConstraint('issue_id', name='issue_pkey'),
        {'schema': 'public'}
    )

    issue_id = mapped_column(Integer)
    user_id = mapped_column(Integer, nullable=False)
    repository_id = mapped_column(Integer, nullable=False)
    title = mapped_column(String(255), nullable=False)
    created_at = mapped_column(DateTime, nullable=False)
    updated_at = mapped_column(DateTime, nullable=False)
    closed_at = mapped_column(DateTime)
    labels_name = mapped_column(ARRAY(String(length=50)))

    repository: Mapped['Repository'] = relationship('Repository', back_populates='issue')
    user: Mapped['UserAccount'] = relationship('UserAccount', back_populates='issue')


class PullRequest(Base):
    __tablename__ = 'pull_request'
    __table_args__ = (
        ForeignKeyConstraint(['repository_id'], ['public.repository.repository_id'], name='pull_request_repository_id_fkey'),
        ForeignKeyConstraint(['user_id'], ['public.user_account.user_id'], name='pull_request_user_id_fkey'),
        PrimaryKeyConstraint('pull_request_id', name='pull_request_pkey'),
        {'schema': 'public'}
    )

    pull_request_id = mapped_column(Integer)
    user_id = mapped_column(Integer, nullable=False)
    repository_id = mapped_column(Integer, nullable=False)
    title = mapped_column(String(255), nullable=False)
    status = mapped_column(String(15), nullable=False)
    created_at = mapped_column(DateTime, nullable=False)
    updated_at = mapped_column(DateTime, nullable=False)
    body = mapped_column(Text)
    closed_at = mapped_column(DateTime)
    merged_at = mapped_column(DateTime)

    repository: Mapped['Repository'] = relationship('Repository', back_populates='pull_request')
    user: Mapped['UserAccount'] = relationship('UserAccount', back_populates='pull_request')
    git_commit: Mapped[List['GitCommit']] = relationship('GitCommit', uselist=True, back_populates='pull_request')


class GitCommit(Base):
    __tablename__ = 'git_commit'
    __table_args__ = (
        ForeignKeyConstraint(['pull_request_id'], ['public.pull_request.pull_request_id'], name='git_commit_pull_request_id_fkey'),
        ForeignKeyConstraint(['repository_id'], ['public.repository.repository_id'], name='git_commit_repository_id_fkey'),
        PrimaryKeyConstraint('commit_id', name='git_commit_pkey'),
        {'schema': 'public'}
    )

    commit_id = mapped_column(CHAR(40))
    pull_request_id = mapped_column(Integer, nullable=False)
    repository_id = mapped_column(Integer, nullable=False)
    commit_message = mapped_column(Text, nullable=False)
    created_at = mapped_column(DateTime, nullable=False)
    html_url = mapped_column(String(255), nullable=False)
    approved_at = mapped_column(DateTime)

    pull_request: Mapped['PullRequest'] = relationship('PullRequest', back_populates='git_commit')
    repository: Mapped['Repository'] = relationship('Repository', back_populates='git_commit')
