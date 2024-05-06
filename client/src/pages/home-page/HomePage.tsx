import { Layout } from './ui/HomePage';
import { PromotionalOffers } from '~widgets/promotional-offers';
import { CategoriesBanner } from '~widgets/categories-banner';
import { SubscribeBlock } from '~widgets/subscribe-block';
import { Banner } from '~widgets/banner';
import { Bestsellers } from '~widgets/bestsellers';
import { NewBlock } from '~widgets/newBlock';

const HomePage = () => (
  <Layout
    banner={<Banner />}
    bestsellers={<Bestsellers />}
    subCategory={<CategoriesBanner />}
    newProducts={<NewBlock />}
    stock={<PromotionalOffers />}
    subscribe={<SubscribeBlock />}
  />
);

export { HomePage };
