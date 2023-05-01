FROM public.ecr.aws/unocha/hdx-data-freshness:main

WORKDIR /srv

RUN pip --no-cache-dir install hdx-data-freshness-dbclean

CMD ["python3", "-m", "hdx.freshness.dbactions"]
