// Copyright (C) 2020-2021 Intel Corporation
//
// SPDX-License-Identifier: MIT

import _cvat from 'cvat-core/src/api';

const cvat: any = _cvat;
const basename: string = '/cvat-annotation';

cvat.config.basename = basename;
cvat.config.backendAPI = `${basename}/api/v1`;

export default function getCore(): any {
    return cvat;
}
