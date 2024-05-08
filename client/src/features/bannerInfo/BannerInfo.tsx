import { Link } from 'react-router-dom';
import css from './BannerInfo.module.scss';

const BannerInfo = () => {
  return (
    <div className={css.bannerInfo}>
      <span className={css.bannerTitle}>
        Innovations for Your Adventure Life: Convenience, Quality, Nature
      </span>
      <Link to="products/:category" className={css.bannerBtn}>
        Shop now
      </Link>
    </div>
  );
};

export { BannerInfo };
