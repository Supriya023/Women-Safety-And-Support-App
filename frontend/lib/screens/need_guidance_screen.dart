import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../models/volunteer_profile_model.dart';
import '../services/api_service.dart';
import '../services/auth_service.dart';
import '../services/notification_service.dart';
import '../theme/app_colors.dart';
import '../widgets/user_shell_layout.dart';
import '../utils/nav_helper.dart';
import 'chatbot_screen.dart';
import 'help_requests_screen.dart';
import 'profile_screen.dart';
import 'volunteer_profiles_screen.dart';

class NeedGuidanceScreen extends StatefulWidget {
  const NeedGuidanceScreen({super.key});

  @override
  State<NeedGuidanceScreen> createState() => _NeedGuidanceScreenState();
}

class _NeedGuidanceScreenState extends State<NeedGuidanceScreen> {
  bool _loadingVolunteers = false;
  List<VolunteerProfileModel> _volunteers = [];

  Future<void> _fetchVolunteers() async {
    setState(() => _loadingVolunteers = true);
    try {
      final token = context.read<AuthService>().token;
      if (token == null) throw Exception('Please login again');
      final response = await ApiService.getVolunteerProfiles(token, onlyActive: false);
      final list = response['volunteers'] as List<dynamic>? ?? [];
      _volunteers = list
          .whereType<Map<String, dynamic>>()
          .map(VolunteerProfileModel.fromJson)
          .toList();
    } catch (err) {
      debugPrint('Error fetching volunteers: $err');
    } finally {
      if (mounted) setState(() => _loadingVolunteers = false);
    }
  }

  Future<void> _requestVolunteerHelp(BuildContext context) async {
    await _fetchVolunteers();

    if (!context.mounted) return;

    final controller = TextEditingController();
    String? selectedVolunteerId;

    final result = await showDialog<Map<String, String>>(
      context: context,
      builder: (context) {
        return StatefulBuilder(
          builder: (context, setDialogState) {
            return AlertDialog(
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(24)),
              title: const Text('Request Volunteer Help', style: TextStyle(fontWeight: FontWeight.bold)),
              content: SingleChildScrollView(
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text('Select a volunteer to assist you:', style: TextStyle(color: AppColors.textMuted, fontSize: 13)),
                    const SizedBox(height: 12),
                    DropdownButtonFormField<String>(
                      decoration: InputDecoration(
                        filled: true,
                        fillColor: AppColors.background,
                        contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
                        border: OutlineInputBorder(borderRadius: BorderRadius.circular(12), borderSide: BorderSide.none),
                        hintText: 'Choose Volunteer',
                      ),
                      value: selectedVolunteerId,
                      items: [
                        const DropdownMenuItem<String>(
                          value: '',
                          child: Text('None (Any Volunteer)', style: TextStyle(fontSize: 14, color: AppColors.textMuted)),
                        ),
                        ..._volunteers.map((v) {
                          return DropdownMenuItem(
                            value: v.id,
                            child: Text(v.name, style: const TextStyle(fontSize: 14)),
                          );
                        }),
                      ],
                      onChanged: (val) => setDialogState(() => selectedVolunteerId = val),
                    ),
                    const SizedBox(height: 20),
                    const Text('Describe what support you need:', style: TextStyle(color: AppColors.textMuted, fontSize: 13)),
                    const SizedBox(height: 12),
                    TextField(
                      controller: controller,
                      maxLines: 3,
                      decoration: InputDecoration(
                        hintText: 'E.g., I need legal advice regarding...',
                        filled: true,
                        fillColor: AppColors.background,
                        border: OutlineInputBorder(borderRadius: BorderRadius.circular(12), borderSide: BorderSide.none),
                      ),
                    ),
                  ],
                ),
              ),
              actions: [
                TextButton(
                  onPressed: () => Navigator.pop(context),
                  child: const Text('Cancel', style: TextStyle(color: AppColors.textMuted)),
                ),
                ElevatedButton(
                  style: ElevatedButton.styleFrom(
                    backgroundColor: AppColors.primary,
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                    padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
                  ),
                  onPressed: () {
                    if (controller.text.trim().isEmpty) {
                      NotificationService.showMessage(context, 'Please enter a description');
                      return;
                    }
                    Navigator.pop(context, {
                      'message': controller.text.trim(),
                      'volunteerId': selectedVolunteerId ?? '',
                    });
                  },
                  child: const Text('Send Request', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
                ),
              ],
            );
          },
        );
      },
    );

    if (result == null) return;
    if (!context.mounted) return;

    try {
      final token = context.read<AuthService>().token;
      if (token == null) throw Exception('Please login again');
      
      await ApiService.createHelpRequest(
        token,
        message: result['message']!,
        volunteerId: result['volunteerId']!.isEmpty ? null : result['volunteerId'],
      );
      
      if (!context.mounted) return;
      NotificationService.showMessage(
          context, 'Help request sent successfully!');
    } catch (err) {
      if (!context.mounted) return;
      NotificationService.showMessage(
        context,
        err.toString().replaceFirst('Exception: ', ''),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    final user = context.watch<AuthService>().currentUser;
    final userName = user?.name ?? 'User';
    return UserShellLayout(
      selectedSection: UserNavSection.needGuidance,
      title: 'Need Guidance',
      subtitle: 'Choose a support type to get the help and guidance you need.',
      userName: userName,
      accountRole: user?.role == 'volunteer' ? 'Volunteer' : 'User',
      onProfileTap: () => NavHelper.replaceWith(context, const ProfileScreen()),
      onLogout: () => context.read<AuthService>().logout(),
      navItems: NavHelper.getNavItems(context, user),
      child: Column(
        children: [
          ShellActionCard(
            title: 'Open Chatbot',
            subtitle:
                'Chat with our AI assistant for quick help and information.',
            icon: Icons.support_agent_rounded,
            iconColor: const Color(0xFF5B34E6),
            iconBackground: const Color(0xFFEDE7FF),
            onTap: () => NavHelper.replaceWith(context, const ChatbotScreen()),
          ),
          ShellActionCard(
            title: 'Request Volunteer Help',
            subtitle: 'Request help from specific verified volunteers.',
            icon: Icons.volunteer_activism_rounded,
            iconColor: const Color(0xFFD9468B),
            iconBackground: const Color(0xFFFFEEF5),
            onTap: () => _requestVolunteerHelp(context),
          ),
          ShellActionCard(
            title: 'View Volunteer Profiles',
            subtitle: 'Browse verified volunteers who can assist you.',
            icon: Icons.groups_2_rounded,
            iconColor: const Color(0xFF169C63),
            iconBackground: const Color(0xFFE9F9F1),
            onTap: () => NavHelper.replaceWith(context, const VolunteerProfilesScreen()),
          ),
          ShellActionCard(
            title: 'View My Help Requests',
            subtitle: 'Track the status of your help requests.',
            icon: Icons.assignment_outlined,
            iconColor: const Color(0xFF5B34E6),
            iconBackground: const Color(0xFFEDE7FF),
            onTap: () => NavHelper.replaceWith(
              context,
              const HelpRequestsScreen(
                isVolunteer: false,
                title: 'My Help Requests',
              ),
            ),
          ),
        ],
      ),
    );
  }
}
