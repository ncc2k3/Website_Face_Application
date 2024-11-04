// assets
import { IconTypography, IconPalette, IconShadow, IconWindmill } from '@tabler/icons';

// constant
const icons = {
    IconTypography,
    IconPalette,
    IconShadow,
    IconWindmill
};

// ==============================|| UTILITIES MENU ITEMS ||============================== //

const faces = {
    id: 'faces',
    title: 'Faces Recognition',
    type: 'group',
    children: [
        {
            id: 'face-detection',
            title: 'Face Detection',
            type: 'item',
            url: '/faces/face-detection',
            icon: icons.IconTypography,
            breadcrumbs: false
        },
        {
            id: 'face-comparision',
            title: 'Face Comparision',
            type: 'item',
            url: '/faces/face-comparision',
            icon: icons.IconTypography,
            breadcrumbs: false
        },
        {
            id: 'face-search',
            title: 'Face Search',
            type: 'item',
            url: '/faces/face-search',
            icon: icons.IconTypography,
            breadcrumbs: false
        },
        {
            id: 'liveness',
            title: 'Liveness (Anti-Spoofing)',
            type: 'item',
            url: '/faces/liveness',
            icon: icons.IconTypography,
            breadcrumbs: false
        },
    ]
};

export default faces;
