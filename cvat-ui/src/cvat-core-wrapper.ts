// Copyright (C) 2020-2021 Intel Corporation
//
// SPDX-License-Identifier: MIT

import _cvat from 'cvat-core/src/api';

const cvat: any = _cvat;
const prefix: string = '/cvat-annotation';

cvat.config.prefix = prefix;
cvat.config.backendAPI = `${prefix}/api/v1`;

export default function getCore(): any {
    return cvat;
}
