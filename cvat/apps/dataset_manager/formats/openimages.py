# Copyright (C) 2021 Intel Corporation
#
# SPDX-License-Identifier: MIT

import glob
import os.path as osp
from tempfile import TemporaryDirectory

from datumaro.components.dataset import Dataset, DatasetItem
from datumaro.plugins.open_images_format import OpenImagesPath
from datumaro.util.image import DEFAULT_IMAGE_META_FILE_NAME
from pyunpack import Archive

from cvat.apps.dataset_manager.bindings import (GetCVATDataExtractor,
    find_dataset_root, import_dm_annotations, match_dm_item)
from cvat.apps.dataset_manager.util import make_zip_archive

from .transformations import RotatedBoxesToPolygons
from .registry import dm_env, exporter, importer


def find_item_ids(path):
    image_desc_patterns = (
        OpenImagesPath.FULL_IMAGE_DESCRIPTION_FILE_NAME,
        *OpenImagesPath.SUBSET_IMAGE_DESCRIPTION_FILE_PATTERNS
    )

    image_desc_patterns = (
        osp.join(path, OpenImagesPath.ANNOTATIONS_DIR, pattern)
        for pattern in image_desc_patterns
    )

    for pattern in image_desc_patterns:
        for path in glob.glob(pattern):
            with open(path, 'r') as desc:
                next(desc)
                for row in desc:
                    yield row.split(',')[0]

@exporter(name='Open Images V6', ext='ZIP', version='1.0')
def _export(dst_file, task_data, save_images=False):
    dataset = Dataset.from_extractors(GetCVATDataExtractor(
        task_data, include_images=save_images), env=dm_env)
    dataset.transform(RotatedBoxesToPolygons)
    dataset.transform('polygons_to_masks')
    dataset.transform('merge_instance_segments')

    with TemporaryDirectory() as temp_dir:
        dataset.export(temp_dir, 'open_images', save_images=save_images)

        make_zip_archive(temp_dir, dst_file)

@importer(name='Open Images V6', ext='ZIP', version='1.0')
def _import(src_file, task_data):
    with TemporaryDirectory() as tmp_dir:
        Archive(src_file.name).extractall(tmp_dir)

        image_meta_path = osp.join(tmp_dir, OpenImagesPath.ANNOTATIONS_DIR,
            DEFAULT_IMAGE_META_FILE_NAME)
        image_meta = None

        if not osp.isfile(image_meta_path):
            image_meta = {}
            item_ids = list(find_item_ids(tmp_dir))

            root_hint = find_dataset_root(
                [DatasetItem(id=item_id) for item_id in item_ids], task_data)

            for item_id in item_ids:
                frame_info = None
                try:
                    frame_id = match_dm_item(DatasetItem(id=item_id),
                        task_data, root_hint)
                    frame_info = task_data.frame_info[frame_id]
                except Exception: # nosec
                    pass
                if frame_info is not None:
                    image_meta[item_id] = (frame_info['height'], frame_info['width'])

        dataset = Dataset.import_from(tmp_dir, 'open_images',
            image_meta=image_meta, env=dm_env)
        dataset.transform('masks_to_polygons')
        import_dm_annotations(dataset, task_data)


