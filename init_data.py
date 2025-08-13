#!/usr/bin/env python3
"""
Initialize sample data for Kèo Sư website
This script populates the database with realistic Vietnamese football content
"""

import os
import sys
from datetime import datetime, timedelta
import random

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import Category, Article, BettingOdd, Match

def create_sample_articles():
    """Create sample articles for different categories"""
    
    # Get categories
    keo_thom = Category.query.filter_by(slug='keo-thom').first()
    soi_keo = Category.query.filter_by(slug='soi-keo').first()
    meo_cuoc = Category.query.filter_by(slug='meo-cuoc').first()
    tin_tuc = Category.query.filter_by(slug='tin-tuc').first()
    
    sample_articles = [
        # Kèo thơm articles
        {
            'title': 'Kèo thơm hôm nay: Manchester United vs Arsenal - Cơ hội vàng cho Quỷ đỏ',
            'slug': 'keo-thom-man-united-vs-arsenal-co-hoi-vang',
            'content': '''
            <h2>Phân tích trận đấu Manchester United vs Arsenal</h2>
            <p>Trận đại chiến giữa Manchester United và Arsenal tại Old Trafford hứa hẹn sẽ là một trong những trận cầu hấp dẫn nhất vòng này của Premier League.</p>
            
            <h3>Phong độ gần đây</h3>
            <p><strong>Manchester United:</strong> Đang có phong độ khá ổn định với 3 trận thắng và 1 hòa trong 4 trận gần nhất. Hàng công của họ đang hoạt động hiệu quả với sự trở lại của Marcus Rashford.</p>
            
            <p><strong>Arsenal:</strong> Pháo thủ đang có chuỗi phong độ không mấy tốt với 2 trận thua liên tiếp. Hàng thủ của họ đang gặp nhiều vấn đề nghiêm trọng.</p>
            
            <h3>Đối đầu trực tiếp</h3>
            <p>Trong 10 trận gần nhất giữa hai đội, Manchester United thắng 6, hòa 2, và thua 2. Đặc biệt, trên sân nhà Old Trafford, MU có phong độ rất tốt trước Arsenal.</p>
            
            <h3>Dự đoán tỷ số và kèo</h3>
            <ul>
                <li><strong>Kèo châu Á:</strong> MU (-0.5) - Tỷ lệ 1.90</li>
                <li><strong>Kèo tài xỉu:</strong> 2.5 - Chọn Tài với tỷ lệ 1.85</li>
                <li><strong>Kèo 1X2:</strong> MU thắng - Tỷ lệ 2.20</li>
            </ul>
            
            <p><strong>Dự đoán:</strong> Manchester United 2-1 Arsenal</p>
            ''',
            'excerpt': 'Phân tích chi tiết trận Manchester United vs Arsenal với những kèo thơm hấp dẫn cho người chơi.',
            'category_id': keo_thom.id if keo_thom else 1,
            'featured': True,
            'meta_title': 'Kèo thơm Man United vs Arsenal - Phân tích chuyên sâu | Kèo Sư',
            'meta_description': 'Phân tích kèo thơm trận Manchester United vs Arsenal với dự đoán tỷ số chính xác và tỷ lệ kèo hấp dẫn.',
            'meta_keywords': 'kèo thơm, manchester united, arsenal, premier league, dự đoán tỷ số',
            'featured_image': 'https://images.unsplash.com/photo-1574629810360-7efbbe195018?w=800'
        },
        
        {
            'title': 'Soi kèo Real Madrid vs Barcelona: El Clasico và những phân tích độc đáo',
            'slug': 'soi-keo-real-madrid-vs-barcelona-el-clasico',
            'content': '''
            <h2>El Clasico - Trận cầu siêu kinh điển</h2>
            <p>Real Madrid vs Barcelona luôn là trận đấu được mong chờ nhất trong mùa giải La Liga. Đây không chỉ là cuộc đối đầu giữa hai đội bóng hàng đầu Tây Ban Nha mà còn là màn so tài giữa hai triết lý bóng đá khác nhau.</p>
            
            <h3>Phân tích lực lượng</h3>
            <p><strong>Real Madrid:</strong> Vinicius Jr. và Benzema đang có phong độ rất cao. Modric vẫn là nhạc trưởng không thể thay thế ở tuyến giữa.</p>
            
            <p><strong>Barcelona:</strong> Lewandowski đã thích nghi tốt với lối chơi của Barca. Pedri và Gavi là những viên ngọc quý của tương lai.</p>
            
            <h3>Thống kê đáng chú ý</h3>
            <ul>
                <li>Real Madrid thắng 7/10 trận gần nhất tại Bernabeu</li>
                <li>Barcelona có tỷ lệ ghi bàn trung bình 2.1 bàn/trận mùa này</li>
                <li>Cả hai đội đều có hàng thủ không quá chắc chắn</li>
            </ul>
            
            <h3>Khuyến nghị đặt cược</h3>
            <p><strong>Kèo chính:</strong> Real Madrid (-0.25) với tỷ lệ 1.95</p>
            <p><strong>Kèo phụ:</strong> Tài 2.5 bàn thắng với tỷ lệ 1.80</p>
            ''',
            'excerpt': 'Phân tích chi tiết trận El Clasico giữa Real Madrid và Barcelona với các khuyến nghị cược hấp dẫn.',
            'category_id': soi_keo.id if soi_keo else 2,
            'featured': True,
            'meta_title': 'Soi kèo Real Madrid vs Barcelona - El Clasico | Kèo Sư',
            'meta_description': 'Soi kèo chuyên sâu trận El Clasico Real Madrid vs Barcelona với phân tích lực lượng và khuyến nghị cược.',
            'meta_keywords': 'soi kèo, real madrid, barcelona, el clasico, la liga',
            'featured_image': 'https://images.unsplash.com/photo-1551698618-1dfe5d97d256?w=800'
        },
        
        {
            'title': 'Mẹo cược bóng đá: 5 chiến thuật quản lý vốn hiệu quả cho người mới',
            'slug': 'meo-cuoc-bong-da-5-chien-thuat-quan-ly-von',
            'content': '''
            <h2>Quản lý vốn - Chìa khóa thành công trong cá cược</h2>
            <p>Quản lý vốn là yếu tố quyết định thành bại của một người chơi cá cược. Dưới đây là 5 chiến thuật hiệu quả được các chuyên gia khuyên dùng.</p>
            
            <h3>1. Quy tắc 1-3% (Kelly Criterion cải tiến)</h3>
            <p>Chỉ đặt cược từ 1-3% tổng vốn cho mỗi trận. Điều này giúp bạn có thể chịu đựng được chuỗi thua mà không bị phá sản.</p>
            <p><strong>Ví dụ:</strong> Nếu có 10 triệu VND, chỉ đặt tối đa 300,000 VND cho một trận.</p>
            
            <h3>2. Chiến thuật Martingale có điều chỉnh</h3>
            <p>Thay vì tăng gấp đôi sau mỗi trận thua, chỉ tăng 50% và có giới hạn số lần áp dụng.</p>
            
            <h3>3. Value Betting - Tìm kiếm giá trị thực</h3>
            <p>So sánh tỷ lệ kèo của nhiều nhà cái để tìm ra những cơ hội có giá trị thật sự cao hơn xác suất thực tế.</p>
            
            <h3>4. Đa dạng hóa danh mục cược</h3>
            <ul>
                <li>Không đặt tất cả vào một giải đấu</li>
                <li>Kết hợp nhiều loại kèo khác nhau</li>
                <li>Cân bằng giữa kèo an toàn và kèo rủi ro cao</li>
            </ul>
            
            <h3>5. Ghi chép và phân tích</h3>
            <p>Luôn ghi lại mọi giao dịch cược để phân tích và rút kinh nghiệm. Sử dụng bảng tính Excel hoặc ứng dụng chuyên dụng.</p>
            
            <h3>Lưu ý quan trọng</h3>
            <p><em>"Không bao giờ cược với tiền không thể mất được. Cá cược là giải trí, không phải cách kiếm sống."</em></p>
            ''',
            'excerpt': '5 chiến thuật quản lý vốn hiệu quả giúp người mới chơi cược bóng đá thành công và bền vững.',
            'category_id': meo_cuoc.id if meo_cuoc else 3,
            'featured': False,
            'meta_title': 'Mẹo cược bóng đá: 5 chiến thuật quản lý vốn cho người mới | Kèo Sư',
            'meta_description': 'Học 5 chiến thuật quản lý vốn hiệu quả trong cá cược bóng đá. Hướng dẫn chi tiết cho người mới bắt đầu.',
            'meta_keywords': 'mẹo cược, quản lý vốn, cá cược bóng đá, kelly criterion, value betting',
            'featured_image': 'https://images.unsplash.com/photo-1560472354-b33ff0c44a43?w=800'
        },
        
        {
            'title': 'Tin tức: Premier League 2024 - Những thay đổi luật và ảnh hưởng đến cược',
            'slug': 'tin-tuc-premier-league-2024-thay-doi-luat',
            'content': '''
            <h2>Premier League 2024: Những thay đổi quan trọng</h2>
            <p>Mùa giải Premier League 2024 đã có những thay đổi quan trọng về luật chơi và quy định, ảnh hưởng trực tiếp đến cách phân tích và đặt cược.</p>
            
            <h3>1. Luật việt vị mới (Semi-automated offside)</h3>
            <p>Công nghệ mới giúp xác định việt vị chính xác hơn, giảm thời gian chờ đợi. Điều này ảnh hưởng đến:</p>
            <ul>
                <li>Số bàn thắng được công nhận tăng lên</li>
                <li>Kèo tài xỉu có thể thay đổi</li>
                <li>Thời gian bù giờ giảm</li>
            </ul>
            
            <h3>2. Quy định VAR được cải tiến</h3>
            <p>VAR chỉ can thiệp vào những tình huống "rõ ràng và sai lầm". Việc này làm giảm số lần dừng trận và tăng tính liên tục của trận đấu.</p>
            
            <h3>3. Luật thẻ vàng cho phản ứng</h3>
            <p>Cầu thủ phản ứng thái quá với quyết định của trọng tài sẽ bị thẻ vàng ngay lập tức. Ảnh hưởng:</p>
            <ul>
                <li>Tăng số thẻ vàng trong trận</li>
                <li>Kèo thẻ phạt trở nên hấp dẫn hơn</li>
            </ul>
            
            <h3>4. Thời gian bù giờ chính xác hơn</h3>
            <p>Trọng tài sẽ tính thời gian bù giờ chính xác hơn, có thể lên đến 8-10 phút. Điều này tạo cơ hội cho:</p>
            <ul>
                <li>Kèo ghi bàn cuối trận</li>
                <li>Kèo tổng số bàn thắng</li>
                <li>Kèo thời gian bù giờ</li>
            </ul>
            
            <h3>Lời khuyên cho người chơi cược</h3>
            <p>Cần theo dõi sát sao những thay đổi này và điều chỉnh chiến thuật cược cho phù hợp. Đặc biệt chú ý đến các trận đấu đầu mùa để nắm bắt xu hướng.</p>
            ''',
            'excerpt': 'Những thay đổi quan trọng trong Premier League 2024 và ảnh hưởng của chúng đến hoạt động cá cược bóng đá.',
            'category_id': tin_tuc.id if tin_tuc else 4,
            'featured': False,
            'meta_title': 'Premier League 2024: Thay đổi luật và ảnh hưởng cược | Kèo Sư',
            'meta_description': 'Cập nhật những thay đổi luật mới trong Premier League 2024 và cách chúng ảnh hưởng đến hoạt động cá cược.',
            'meta_keywords': 'premier league 2024, thay đổi luật, tin tức bóng đá, var, việt vị',
            'featured_image': 'https://images.unsplash.com/photo-1508098682722-e99c43a406b2?w=800'
        },
        
        {
            'title': 'Kèo thơm cuối tuần: Bayern Munich vs Dortmund - Derby nước Đức',
            'slug': 'keo-thom-bayern-munich-vs-dortmund-derby-duc',
            'content': '''
            <h2>Der Klassiker - Trận cầu kinh điển nước Đức</h2>
            <p>Bayern Munich vs Borussia Dortmund luôn là trận đấu được chờ đợi nhất trong mỗi mùa giải Bundesliga. Đây là cuộc đối đầu giữa hai ứng cử viên hàng đầu cho chức vô địch.</p>
            
            <h3>Tình hình lực lượng</h3>
            <p><strong>Bayern Munich:</strong></p>
            <ul>
                <li>Harry Kane đang có phong độ ghi bàn ấn tượng</li>
                <li>Musiala và Sane tạo nên hàng công đáng sợ</li>
                <li>Hàng thủy có Upamecano và De Ligt rất chắc chắn</li>
            </ul>
            
            <p><strong>Borussia Dortmund:</strong></p>
            <ul>
                <li>Haaland đã ra đi nhưng có những bổ sung chất lượng</li>
                <li>Bellingham vẫn là động cơ của đội</li>
                <li>Hàng phòng ngự là điểm yếu cần chú ý</li>
            </ul>
            
            <h3>Phân tích kèo cược</h3>
            <table border="1" style="width: 100%; border-collapse: collapse;">
                <tr>
                    <th>Loại kèo</th>
                    <th>Tỷ lệ</th>
                    <th>Khuyến nghị</th>
                </tr>
                <tr>
                    <td>Châu Á (-0.75)</td>
                    <td>1.90</td>
                    <td>Bayern Munich</td>
                </tr>
                <tr>
                    <td>Tài Xỉu (3.25)</td>
                    <td>1.85</td>
                    <td>Tài</td>
                </tr>
                <tr>
                    <td>1X2</td>
                    <td>1.75</td>
                    <td>Bayern thắng</td>
                </tr>
            </table>
            
            <h3>Dự đoán kết quả</h3>
            <p><strong>Tỷ số dự đoán:</strong> Bayern Munich 3-1 Borussia Dortmund</p>
            <p><strong>Lý do:</strong> Bayern có lợi thế sân nhà và đội hình mạnh hơn toàn diện.</p>
            ''',
            'excerpt': 'Phân tích kèo thơm trận Derby nước Đức giữa Bayern Munich và Dortmund với dự đoán chi tiết.',
            'category_id': keo_thom.id if keo_thom else 1,
            'featured': True,
            'views': random.randint(150, 500),
            'meta_title': 'Kèo thơm Bayern vs Dortmund - Der Klassiker | Kèo Sư',
            'meta_description': 'Phân tích kèo thơm trận Bayern Munich vs Dortmund với dự đoán tỷ số và tỷ lệ cược hấp dẫn.',
            'meta_keywords': 'kèo thơm, bayern munich, dortmund, bundesliga, der klassiker',
            'featured_image': 'https://images.unsplash.com/photo-1553778263-73a83bab9b0c?w=800'
        }
    ]
    
    # Create articles
    for article_data in sample_articles:
        # Check if article already exists
        existing = Article.query.filter_by(slug=article_data['slug']).first()
        if not existing:
            # Generate random views if not specified
            if 'views' not in article_data:
                article_data['views'] = random.randint(50, 300)
            
            article = Article(**article_data)
            db.session.add(article)
    
    try:
        db.session.commit()
        print(f"✅ Created {len(sample_articles)} sample articles")
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error creating articles: {e}")

def create_sample_betting_odds():
    """Create sample betting odds for today and tomorrow"""
    
    today = datetime.now()
    tomorrow = today + timedelta(days=1)
    
    matches_data = [
        {
            'home_team': 'Manchester United',
            'away_team': 'Arsenal',
            'match_date': today.replace(hour=21, minute=0),
            'league': 'Premier League',
            'home_win': 2.20,
            'draw': 3.40,
            'away_win': 3.10,
            'over_2_5': 1.85,
            'under_2_5': 1.95,
            'handicap': '-0.5',
            'handicap_home': 1.90,
            'handicap_away': 1.90,
            'recommendation': 'Chủ nhà thắng',
            'confidence': 4
        },
        {
            'home_team': 'Real Madrid',
            'away_team': 'Barcelona',
            'match_date': today.replace(hour=23, minute=30),
            'league': 'La Liga',
            'home_win': 1.95,
            'draw': 3.60,
            'away_win': 3.80,
            'over_2_5': 1.70,
            'under_2_5': 2.10,
            'handicap': '-0.25',
            'handicap_home': 1.95,
            'handicap_away': 1.85,
            'recommendation': 'Tài 2.5',
            'confidence': 5
        },
        {
            'home_team': 'Bayern Munich',
            'away_team': 'Borussia Dortmund',
            'match_date': tomorrow.replace(hour=20, minute=30),
            'league': 'Bundesliga',
            'home_win': 1.75,
            'draw': 4.00,
            'away_win': 4.50,
            'over_2_5': 1.65,
            'under_2_5': 2.25,
            'handicap': '-0.75',
            'handicap_home': 1.88,
            'handicap_away': 1.92,
            'recommendation': 'Chủ nhà -0.75',
            'confidence': 4
        },
        {
            'home_team': 'Liverpool',
            'away_team': 'Chelsea',
            'match_date': tomorrow.replace(hour=22, minute=0),
            'league': 'Premier League',
            'home_win': 2.10,
            'draw': 3.20,
            'away_win': 3.40,
            'over_2_5': 1.80,
            'under_2_5': 2.00,
            'handicap': '-0.25',
            'handicap_home': 1.92,
            'handicap_away': 1.88,
            'recommendation': 'Xỉu 2.5',
            'confidence': 3
        },
        {
            'home_team': 'Juventus',
            'away_team': 'AC Milan',
            'match_date': today.replace(hour=19, minute=45),
            'league': 'Serie A',
            'home_win': 2.35,
            'draw': 3.10,
            'away_win': 2.95,
            'over_2_5': 1.90,
            'under_2_5': 1.90,
            'handicap': '0',
            'handicap_home': 1.85,
            'handicap_away': 1.95,
            'recommendation': 'Khách 0',
            'confidence': 3
        }
    ]
    
    for match_data in matches_data:
        # Create betting odd entry
        match_name = f"{match_data['home_team']} vs {match_data['away_team']}"
        match_data['match_name'] = match_name
        
        # Check if already exists
        existing = BettingOdd.query.filter_by(
            home_team=match_data['home_team'],
            away_team=match_data['away_team'],
            match_date=match_data['match_date']
        ).first()
        
        if not existing:
            odd = BettingOdd(**match_data)
            db.session.add(odd)
    
    try:
        db.session.commit()
        print(f"✅ Created {len(matches_data)} betting odds")
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error creating betting odds: {e}")

def create_sample_matches():
    """Create sample match schedule"""
    
    today = datetime.now()
    
    matches_schedule = []
    
    # Generate matches for next 7 days
    for i in range(7):
        match_date = today + timedelta(days=i)
        
        # Add 2-3 matches per day
        daily_matches = [
            {
                'home_team': 'Manchester City',
                'away_team': 'Tottenham',
                'match_date': match_date.replace(hour=20, minute=0),
                'league': 'Premier League',
                'venue': 'Etihad Stadium',
                'status': 'scheduled'
            },
            {
                'home_team': 'PSG',
                'away_team': 'Lyon',
                'match_date': match_date.replace(hour=22, minute=0),
                'league': 'Ligue 1',
                'venue': 'Parc des Princes',
                'status': 'scheduled'
            }
        ]
        
        matches_schedule.extend(daily_matches)
    
    # Add some finished matches with scores
    finished_matches = [
        {
            'home_team': 'Arsenal',
            'away_team': 'Chelsea',
            'match_date': today - timedelta(days=1),
            'league': 'Premier League',
            'venue': 'Emirates Stadium',
            'status': 'finished',
            'home_score': 2,
            'away_score': 1
        },
        {
            'home_team': 'Real Madrid',
            'away_team': 'Atletico Madrid',
            'match_date': today - timedelta(days=2),
            'league': 'La Liga',
            'venue': 'Santiago Bernabeu',
            'status': 'finished',
            'home_score': 3,
            'away_score': 1
        }
    ]
    
    matches_schedule.extend(finished_matches)
    
    for match_data in matches_schedule:
        # Check if already exists
        existing = Match.query.filter_by(
            home_team=match_data['home_team'],
            away_team=match_data['away_team'],
            match_date=match_data['match_date']
        ).first()
        
        if not existing:
            match = Match(**match_data)
            db.session.add(match)
    
    try:
        db.session.commit()
        print(f"✅ Created {len(matches_schedule)} match schedules")
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error creating matches: {e}")

def main():
    """Main function to initialize all sample data"""
    print("🚀 Initializing sample data for Kèo Sư website...")
    
    with app.app_context():
        # Create sample articles
        create_sample_articles()
        
        # Create sample betting odds
        create_sample_betting_odds()
        
        # Create sample matches
        create_sample_matches()
        
        print("✅ Sample data initialization completed!")
        print("\n📊 Database Summary:")
        print(f"   • Categories: {Category.query.count()}")
        print(f"   • Articles: {Article.query.count()}")
        print(f"   • Betting Odds: {BettingOdd.query.count()}")
        print(f"   • Matches: {Match.query.count()}")
        print("\n🌐 You can now start the website with: python main.py")

if __name__ == '__main__':
    main()
