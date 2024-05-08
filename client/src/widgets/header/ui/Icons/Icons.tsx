import cn from 'classnames';
// import { useState } from 'react';

import { Icon } from '~shared/ui/Icon';

import css from './Icons.module.scss';

const Icons = () => {
  // const [cartCount] = useState(1);

  return (
    <div className={css.icons}>
      <Icon className={cn(css.icon, css.mobHide)} type="like" />
      <div className={css.iconBtn}>
        <Icon className={css.icon} type="cart" />
        {/* <span className={css.cartCount}>{cartCount}</span> */}
      </div>
    </div>
  );
};

export { Icons };
