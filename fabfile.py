from fabric.api import env, run, sudo, cd, execute, prefix

# TODO: переделать fabric на локальный запуск, тогда он будет универсальным
# для локального, тестового и продакшн деплоймента.
# деплоймент на сервера должен заходить на сервер, переходить в директорию
# проекта, инициализировать окружение и запускать локальный деплоймент

# TODO: реализовать init_database которая будет мигрировать БД,
# накатывать фикстуты, создавать суперпользователя

# TODO: https://samoylov.tech/2016/09/29/deploying-django-with-fabric/

env.roledefs = {
    'test': [
        'alex@89.108.108.225:2222',
    ],
}

FIXTURES = ()
BASE_DIR = '/var/www/volunteer.1m8.ru'
PROJECT_NAME = 'volunteer'
PROJECT_DIR = '{0}/backend'.format(BASE_DIR)
ENV_ACTIVATE = '{0}/env/bin/activate'.format(BASE_DIR)


def deploy(role='test'):
    execute(_update_project, role=role)
    execute(_migrate_databases, role=role)
    execute(_collect_static, role=role)
    execute(_restart_project, role=role)


def update_project(role='test'):
    execute(_update_project, role=role)


def install_requirements(role='test'):
    execute(_install_requirements, role=role)


def load_fixture(fixture, role='test'):
    execute(_load_fixtures, role=role, fixture=fixture)


def load_all_fixtures(role='test'):
    execute(_load_fixtures, role=role)


def _update_project():
    with cd(PROJECT_DIR):
        run('git pull')


def _restart_project():
    sudo('supervisorctl restart {0}:'.format(PROJECT_NAME))


def _collect_static():
    with cd(PROJECT_DIR), prefix('source {0}'.format(ENV_ACTIVATE)):
        run('echo "yes" | python src/manage.py collectstatic')


def _migrate_databases():
    with cd(PROJECT_DIR), prefix('source {0}'.format(ENV_ACTIVATE)):
        run('python src/manage.py migrate')


def _install_requirements(update=True):
    with cd(PROJECT_DIR), prefix('source {0}'.format(ENV_ACTIVATE)):
        if update:
            run('pip install -U -r requirements.txt')
        else:
            run('pip install -r requirements.txt')


def _uninstall_requirements(packages=None):
    if packages:
        with cd(PROJECT_DIR), prefix('source {0}'.format(ENV_ACTIVATE)):
            run('pip uninstall -y {0}'.format(packages))


def _load_fixtures(fixture=None):
    with cd(PROJECT_DIR), prefix('source {0}'.format(ENV_ACTIVATE)):
        fixtures = [fixture] if fixture else FIXTURES

        for name in fixtures:
            run('python src/manage.py loaddata {0}'.format(name))
