"""Add LogLevel and LogStatus enums and logs table

Revision ID: 12
Revises: 11
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSON


# revision identifiers, used by Alembic.
revision: str = "12"
down_revision: Union[str, None] = "11"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema - add LogLevel and LogStatus enums and logs table."""
    
    # Create LogLevel enum
    op.execute("""
        CREATE TYPE loglevel AS ENUM ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')
    """)
    
    # Create LogStatus enum  
    op.execute("""
        CREATE TYPE logstatus AS ENUM ('IN_PROGRESS', 'SUCCESS', 'FAILED')
    """)
    
    # Create logs table
    op.execute("""
        CREATE TABLE logs (
            id SERIAL PRIMARY KEY,
            created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
            level loglevel NOT NULL,
            status logstatus NOT NULL,
            message TEXT NOT NULL,
            source VARCHAR(200),
            log_metadata JSONB DEFAULT '{}',
            search_space_id INTEGER NOT NULL REFERENCES searchspaces(id) ON DELETE CASCADE
        )
    """)
    
    # Create indexes
    op.create_index(op.f('ix_logs_id'), 'logs', ['id'], unique=False)
    op.create_index(op.f('ix_logs_created_at'), 'logs', ['created_at'], unique=False)
    op.create_index(op.f('ix_logs_level'), 'logs', ['level'], unique=False)
    op.create_index(op.f('ix_logs_status'), 'logs', ['status'], unique=False)
    op.create_index(op.f('ix_logs_source'), 'logs', ['source'], unique=False)


def downgrade() -> None:
    """Downgrade schema - remove logs table and enums."""
    
    # Drop indexes
    op.drop_index(op.f('ix_logs_source'), table_name='logs')
    op.drop_index(op.f('ix_logs_status'), table_name='logs')
    op.drop_index(op.f('ix_logs_level'), table_name='logs')
    op.drop_index(op.f('ix_logs_created_at'), table_name='logs')
    op.drop_index(op.f('ix_logs_id'), table_name='logs')
    
    # Drop logs table
    op.drop_table('logs')
    
    # Drop enums
    op.execute("DROP TYPE IF EXISTS logstatus")
    op.execute("DROP TYPE IF EXISTS loglevel") 