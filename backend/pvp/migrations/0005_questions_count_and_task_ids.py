from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pvp', '0004_legacy_notnull_defaults_compat'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunSQL(
                    sql="""
                        ALTER TABLE pvp_match
                        ADD COLUMN IF NOT EXISTS question_task_ids jsonb NOT NULL DEFAULT '[]'::jsonb;

                        ALTER TABLE pvp_match
                        ADD COLUMN IF NOT EXISTS questions_count smallint NOT NULL DEFAULT 1;

                        UPDATE pvp_match
                        SET question_task_ids = jsonb_build_array(task_id)
                        WHERE task_id IS NOT NULL
                          AND question_task_ids = '[]'::jsonb;

                        UPDATE pvp_match
                        SET questions_count = GREATEST(
                            1,
                            COALESCE(questions_count, 1)
                        );
                    """,
                    reverse_sql=migrations.RunSQL.noop,
                )
            ],
            state_operations=[
                migrations.AddField(
                    model_name='match',
                    name='question_task_ids',
                    field=models.JSONField(blank=True, default=list),
                ),
                migrations.AddField(
                    model_name='match',
                    name='questions_count',
                    field=models.PositiveSmallIntegerField(default=1),
                ),
            ],
        ),
    ]
