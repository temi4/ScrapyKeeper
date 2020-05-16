import threading
from datetime import datetime, timedelta
import time

from ScrapyKeeper.app import scheduler, app, agent, db
from ScrapyKeeper.app.spider.model import Project, JobInstance, SpiderInstance, SpiderStatus, JobExecution


def sync_job_execution_status_job():
    '''
    sync job execution running status
    :return:
    '''
    for project in Project.query.all():
        agent.sync_job_status(project)
    app.logger.debug('[sync_job_execution_status]')


def sync_spiders():
    '''
    sync spiders
    :return:
    '''
    for project in Project.query.all():
        spider_instance_list = agent.get_spider_list(project)
        SpiderInstance.update_spider_instances(project.id, spider_instance_list)
    app.logger.debug('[sync_spiders]')


def run_spider_job(job_instance_id):
    '''
    run spider by scheduler
    :param job_instance_id:
    :return:
    '''
    try:
        job_instance = JobInstance.find_job_instance_by_id(job_instance_id)
        start_tasks = job_instance.start_tasks

        """start_time = datetime.now() - timedelta(minutes=30)
        count = JobExecution.query.filter_by(
            job_instance_id=job_instance_id,
            running_status=SpiderStatus.RUNNING,
        ).filter(JobExecution.start_time < start_time).count()
        if count > 0:
            return"""

        count = JobExecution.query.filter_by(job_instance_id=job_instance_id).filter(
            JobExecution.running_status.in_([SpiderStatus.PENDING, SpiderStatus.RUNNING])
        ).count()
        if count >= job_instance.max_start_tasks:
            return

        slots = job_instance.max_start_tasks - count
        if job_instance.start_tasks > slots:
            start_tasks = slots

        if start_tasks > 0:
            i = 0
            while i < start_tasks:
                agent.start_spider(job_instance)
                i += 1
                app.logger.info(
                    '[run_spider_job][project:%s][spider_name:%s][job_instance_id:%s]'
                    '[start_tasks:%s][i:%s]' % (
                    job_instance.project_id, job_instance.spider_name, job_instance.id, start_tasks, i))

    except Exception as e:
        app.logger.error('[run_spider_job] ' + str(e))


def reload_runnable_spider_job_execution():
    '''
    add periodic job to scheduler
    :return:
    '''
    running_job_ids = set([job.id for job in scheduler.get_jobs()])
    app.logger.debug('[running_job_ids] %s' % ','.join(running_job_ids))
    available_job_ids = set()
    # add new job to schedule
    for job_instance in JobInstance.query.filter_by(enabled=0, run_type="periodic").all():
        app.logger.debug('[start job_instance] %s' % job_instance.id)
        job_id = "spider_job_%s:%s" % (job_instance.id, int(time.mktime(job_instance.date_modified.timetuple())))
        available_job_ids.add(job_id)
        if job_id not in running_job_ids:
            try:
                scheduler.add_job(run_spider_job,
                                  args=(job_instance.id,),
                                  trigger='cron',
                                  id=job_id,
                                  minute=job_instance.cron_minutes,
                                  hour=job_instance.cron_hour,
                                  day=job_instance.cron_day_of_month,
                                  day_of_week=job_instance.cron_day_of_week,
                                  month=job_instance.cron_month,
                                  second=0,
                                  max_instances=999,
                                  misfire_grace_time=60 * 60,
                                  coalesce=True)
            except Exception as e:
                app.logger.error(
                    '[load_spider_job] failed {} {},may be cron expression format error '.format(job_id, str(e)))
            app.logger.info('[load_spider_job][project:%s][spider_name:%s][job_instance_id:%s][job_id:%s]' % (
                job_instance.project_id, job_instance.spider_name, job_instance.id, job_id))
    # remove invalid jobs
    for invalid_job_id in filter(lambda job_id: job_id.startswith("spider_job_"),
                                 running_job_ids.difference(available_job_ids)):
        scheduler.remove_job(invalid_job_id)
        app.logger.info('[drop_spider_job][job_id:%s]' % invalid_job_id)
