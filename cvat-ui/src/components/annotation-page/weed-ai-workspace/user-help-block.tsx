// Copyright (C) 2020-2021 Intel Corporation
//
// SPDX-License-Identifier: MIT

import React, { Dispatch } from 'react';
import { AnyAction } from 'redux';
import { connect } from 'react-redux';
import Text from 'antd/lib/typography/Text';
import Collapse from 'antd/lib/collapse';

import { CombinedState } from 'reducers/interfaces';
import { collapseUserHelp as collapseUserHelpAction } from 'actions/annotation-actions';

interface StateToProps {
    userHelpCollapsed: boolean;
}

interface DispatchToProps {
    collapseUserHelp(): void;
}

function mapStateToProps(state: CombinedState): StateToProps {
    const {
        annotation: {
            userHelpCollapsed,
        },
    } = state;

    return {
        userHelpCollapsed,
    };
}

function mapDispatchToProps(dispatch: Dispatch<AnyAction>): DispatchToProps {
    return {
        collapseUserHelp(): void {
            dispatch(collapseUserHelpAction());
        },
    };
}

type Props = StateToProps & DispatchToProps;

function UserHelpBlock(props: Props): JSX.Element {
    const {
        userHelpCollapsed,
        collapseUserHelp,
    } = props;

    return (
        <Collapse
            onChange={collapseUserHelp}
            activeKey={userHelpCollapsed ? [] : ['userhelp']}
            className='cvat-objects-user-help-collapse'
        >
            <Collapse.Panel
                header={(
                    <Text strong className='cvat-objects-user-help-collapse-header'>
                        Annotation guide
                    </Text>
                )}
                key='userhelp'
            >
                <div className='cvat-objects-user-help-content'>
                    Some text to help the user with a
                    {' '}
                    <a href='https://weed-ai.sydney.edu.au/'>link</a>
                    {' '}
                    to further info
                </div>
            </Collapse.Panel>
        </Collapse>
    );
}

export default connect(mapStateToProps, mapDispatchToProps)(React.memo(UserHelpBlock));
