// Copyright (C) 2020-2021 Intel Corporation
//
// SPDX-License-Identifier: MIT

import _cvat from 'cvat-core/src/api';
import config from './config';

const cvat: any = _cvat;
const basename: string = config.basename;

cvat.config.basename = basename;
cvat.config.backendAPI = `${basename}/api/v1`;

export default function getCore(): any {
    return cvat;
}
