FROM project-dummy:devel-0.1
COPY conf conf
COPY api api
COPY project_dummy project_dummy
ADD config config
COPY utilities utilities
ADD main.py .
ADD start_entrypoint.sh .

ENTRYPOINT ["/bin/bash", "start_entrypoint.sh"]