// assets
import { IconEye, IconSearch, IconScale, IconHeartbeat } from '@tabler/icons';

// Các icon mới sẽ là:
// - IconEye cho Face Detection
// - IconSearch cho Search
// - IconScale cho Comparison
// - IconHeartbeat cho Liveness


// constant
const icons = {
    IconEye,
    IconSearch,
    IconScale,
    IconHeartbeat
};

// ==============================|| FACES MENU ITEMS ||============================== //

const faces = {
    id: 'faces',
    title: 'Faces',
    caption: 'Face Recognition',
    type: 'group',
    children: [
        {
            id: 'face-detection',
            title: 'Face Detection',
            type: 'item',
            url: '/faces/face-detection',
            icon: icons.IconEye,
            breadcrumbs: false
        },
        {
            id: 'face-comparision',
            title: 'Face Comparision',
            type: 'item',
            url: '/faces/face-comparision',
            icon: icons.IconScale,
            breadcrumbs: false
        },
        {
            id: 'face-search',
            title: 'Face Search',
            type: 'item',
            url: '/faces/face-search',
            icon: icons.IconSearch,
            breadcrumbs: false
        },
        {
            id: 'liveness',
            title: 'Liveness (Anti-Spoofing)',
            type: 'item',
            url: '/faces/liveness',
            icon: icons.IconHeartbeat,
            breadcrumbs: false
        },
    ]
};

export default faces;
