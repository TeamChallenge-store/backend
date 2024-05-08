import { SubscribeForm } from '~features/subscribe-form';
import css from './SubscribeBlock.module.scss';

const SubscribeBlock = () => {
  return (
    <div className={`${css.subscribe} container`}>
      <h1 className={css.title}>Innovations for Your Adventure Life</h1>
      <div className={css.formContainer}>
        <div className={css.form}>
          <SubscribeForm />
        </div>
        <span className={css.formDescription}>
          Embark on your next adventure with confidence. Explore the world with
          our top-quality gear by your side. Start your journey today!
        </span>
      </div>
    </div>
  );
};

export { SubscribeBlock };
